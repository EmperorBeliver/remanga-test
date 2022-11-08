from django.http.response import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from .models import TitleModel, ChapterModel
from .utils import *
from .tasks import *

# Create your views here.
def main(request):
    return HttpResponse()

@api_view(['GET'])
def titles(request):
    titles = list(TitleModel.objects.all())
    answer = {
        "msg": '',
        "content": []
    }
    if(len(titles) == 0):
        answer['msg'] = 'Нет книг'
        return JsonResponse(answer, safe=False, json_dumps_params={'ensure_ascii': False})

    if(request.GET.get('count', None) != None):
        count = int(request.GET.get('count'))
        if(len(titles) < count):
            count = len(titles) 
        answer["content"] = get_list_titles(titles, count)    
        return JsonResponse(answer, safe=False, json_dumps_params={'ensure_ascii': False})
    
    answer["content"] = get_list_titles(titles, len(titles))
    return JsonResponse(answer, safe=False, json_dumps_params={'ensure_ascii': False})

@api_view(['GET'])
def titles_details(request):
    titles = list(TitleModel.objects.all())
    answer = {
        'msg': '',
        'content': []
    }

    if(len(titles) == 0):
        answer['msg'] = 'Нет книг'
        return JsonResponse(answer)

    for title in titles:
        answer['content'].append({
            "rus_name": title.rus_name,
            "eng_name": title.eng_name,
            "other_name": title.other_name,
            "desc": title.desc,
            "tags": get_list_tags(title),
            "volumes": get_list_volume(title),
            "chapters": get_list_chapters(title)
        })
        
    return JsonResponse(answer, safe=False, json_dumps_params={'ensure_ascii': False})

@api_view(['GET'])
def chapter(request): 
    answer = {
        "msg": '',
        "content": []
    }

    if(request.GET.get('id', None) == None):
        return HttpResponse(status=428)

    chapter_id = int(request.GET.get('id'))
    try:
        chapter = ChapterModel.objects.get(id=chapter_id)

    except ObjectDoesNotExist:
        answer['msg'] = 'Нет главы!'
        return JsonResponse(answer, safe=False, json_dumps_params={'ensure_ascii': False})

    increment_views(chapter)

    answer['content'].append({
        "volume": chapter.volume.title.rus_name,
        "count": chapter.count,
        "views": chapter.views,
        "likes": chapter.likes,
        "content": chapter.content
    })

    return JsonResponse(answer, safe=False, json_dumps_params={'ensure_ascii': False})

@api_view(['GET'])
def like_chapter(request):
    answer = {
        "msg": '',
        "content": []
    }

    if(request.GET.get('id', None) == None):
        return HttpResponse(status=428)

    chapter_id = int(request.GET.get('id'))
    try:
        chapter = ChapterModel.objects.get(id=chapter_id)

    except ObjectDoesNotExist:
        answer['msg'] = 'Нет главы!'
        return JsonResponse(answer, safe=False, json_dumps_params={'ensure_ascii': False})

    increment_likes(chapter)

    answer['content'].append({
        "volume": chapter.volume.title.rus_name,
        "likes": chapter.likes
    })

    return JsonResponse(answer, safe=False, json_dumps_params={'ensure_ascii': False})
