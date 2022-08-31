import pandas as pd
import random
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from sklearn import svm

class Sentiment:
    NEGATIVE = 'NEGATIVE'
    POSITVIE = 'POSITIVE'
    NEUTRAL = 'NEUTRAL'

class Response:
    def __init__(self, score, text):
        self.score = score
        self.text = text
        self.sentiment = self.get_sentiment()
    
    def get_sentiment(self):
        if self.score == 1:
            return Sentiment.NEGATIVE
        elif self.score == 2:
            return Sentiment.POSITVIE
        else:
            return Sentiment.NEUTRAL

class ReviewContainer:
    def __init__(self, reviews):
        self.reviews = reviews

    def get_text(self):
        return [x.text for x in self.reviews]

    def get_sentiment(self):
        return [x.sentiment for x in self.reviews]

    def get_score(self):
        return [x.score for x in self.reviews]

    def evenely_distribute(self):
        negative = list(filter(lambda x: x.sentiment == Sentiment.NEGATIVE, self.reviews))
        positive = list(filter(lambda x: x.sentiment == Sentiment.POSITVIE, self.reviews))
        positive_adjusted = positive[:len(negative)]
        self.reviews = negative + positive_adjusted
        random.shuffle(self.reviews)

df = pd.read_csv('AmazonReviews.csv', delimiter=',')

comment_sentiments = [Response(tuple(row)[0], tuple(row)[1]) for row in df.values]

training,test = train_test_split(comment_sentiments, test_size=0.2, random_state=42)

train_container = ReviewContainer(training)
train_container.evenely_distribute()

test_container = ReviewContainer(test)

train_x = train_container.get_text()
train_y = train_container.get_score()

test_x = test_container.get_text()
test_y = test_container.get_score()

vectorizer = TfidfVectorizer()
train_x_vectors = vectorizer.fit_transform(train_x)
with open('vectorizer.pickle', 'wb') as f1:
    pickle.dump(vectorizer, f1)
test_x_vectors = vectorizer.transform(test_x)

clf_svm = svm.SVC(kernel='linear')
clf_svm.fit(train_x_vectors, train_y)

with open('sentiment_classifier.pickle', 'wb') as f2:
   pickle.dump(clf_svm, f2)