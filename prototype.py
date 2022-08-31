from googleapiclient.discovery import build
import pandas as pd
import re
import pickle

api_key = "AIzaSyCO4eac7ghuYRPoY6ZtAqvIstpwW2F2NSQ"
resource = build('youtube', 'v3', developerKey=api_key)

def get_comments(id): #extracts the top 300 comments from a youtube video
    comments = []
    
    response = resource.commentThreads().list(
        part='snippet',
        videoId=id,
        maxResults = 100,
        order = 'relevance'
    ).execute() #create a request for a page of up to 100 comments

    i = 0
    while i<3 and response:
        i+=1
        for item in response['items']: #append each comment from request to a list of comments
            # load comment into list
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
  
        # search next page of comments
        if 'nextPageToken' in response: #checks if a new page of comments is available and subsequently makes a new request
            p_token = response['nextPageToken']
            response = resource.commentThreads().list(
                    part = 'snippet',
                    videoId = id,
                    maxResults = 100,
                    order = 'relevance',
                    pageToken = p_token
                ).execute()
        else:
            break
    return comments

def clean_text(comment):
    comment = re.sub(r'@[A-Za-z0-9]+', '', comment) #removes @mentions
    comment = re.sub(r'#', '', comment) #removes hashtags
    comment = re.sub(r'<a href="https?:\/\/\S+', '', comment) #removes hyperlinked comments
    return comment

def get_polarity(comment_list):
    vector_file = open('training_model/vectorizer.pickle', 'rb')
    classifier_file = open('training_model/sentiment_classifier.pickle', 'rb')
    vectorizer = pickle.load(vector_file)
    clf_svm = pickle.load(classifier_file)
    comment_vectors = vectorizer.transform(comment_list)
    polarity = clf_svm.predict(comment_vectors)
    vector_file.close()
    classifier_file.close()
    return polarity

def score_video(url):
    youtube = "https://www.youtube.com/watch?v="
    youtube_shorts = "https://www.youtube.com/shorts/"

    if (url.startswith(youtube)):
        video_id = url.replace(youtube,"")
    elif (url.startswith(youtube_shorts)):
        video_id = url.replace(youtube_shorts,"")
    else:
        return [-1, 0.0, 0.0, 0.0, 0]

    try: 
        comments = get_comments(video_id)
    except:
        return [0, 0.0, 0.0, 0.0, 0] #comments are restricted, unable to analyze sentiments

    df = pd.DataFrame(comments, columns=['Comments']) #comments not restricted so create dataframe to store comments
    df['Polarity'] = get_polarity(df['Comments'])

    top_comments_score = 0 #top 20% comments are weighted more than the rest
    bottom_comments_score = 0
    positive_count = 0  #tracks the number of positive comments
    comments_count = len(comments)
    top_comments_count = int(0.2*comments_count) 

    for i in range(top_comments_count): #calculates a score for the first 20% of comments
        if df['Polarity'][i] == 2:
            positive_count+=1
            top_comments_score+=1

    for i in range(top_comments_count, comments_count): #calculates a score for the rest of comments
        if df['Polarity'][i] == 2:
            positive_count+=1
            bottom_comments_score+=1

    top_comments_score = top_comments_score / top_comments_count #averages the score of the top comments
    bottom_comments_score = bottom_comments_score / (comments_count - top_comments_count) #averages the score of the bottom comments
    score = 5*(top_comments_score + bottom_comments_score) / 2 #creates a score out of five
    percent_positive = positive_count/comments_count
    percent_negative = 1-percent_positive
    return [1, score, percent_positive, percent_negative, comments_count] # returns success, score, percent positive, and percent negative

def main():
    url = input("Enter url for a youtube video:\t")

    x = score_video(url)
    print(x)

if __name__ == "__main__":
    main()