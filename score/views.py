from django.shortcuts import render

from django.http import JsonResponse,HttpResponse

import prototype

def get_score(request):
    topic = request.GET.get('topic', None)
    response = prototype.score_video(topic)
    data = {
        'success': response[0],
        'score': round(response[1],1),
        'percent_positive': round((100*response[2]),1),
        'percent_negative': round((100*response[3]),1),
        'positive_bar': str(int(145*response[2]))+"px",
        'negative_bar': str(int(145*response[3]))+"px",
        'comment_count': response[4]
    }
    return JsonResponse(data)
