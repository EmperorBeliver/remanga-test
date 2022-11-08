from .models import VolumeModel, ChapterModel
from .tasks import increment_views
from asgiref.sync import sync_to_async

# Get list of title's tags
def get_list_tags(title):
    tags = []
    for tag in list(title.tags.all()):
            tags.append(tag.name)
    return tags

# Get list of titles information
def get_list_titles(titles: list, count: int) -> list:
    answer = []
    for i in range(count):
        answer.append({
            "rus_name": titles[i].rus_name,
            "eng_name": titles[i].eng_name,
            "other_name": titles[i].other_name,
            "desc": titles[i].desc,
            "tags": get_list_tags(titles[i])
        })
    return answer

# Get list of volumes information
def get_list_volume(title):
    formated_volumes = []
    query_volumes = list(VolumeModel.objects.filter(title__rus_name=title.rus_name))
    
    for volume in query_volumes:
        formated_volumes.append({
            "name": volume.name,
            "cost": volume.cost,
            "number": volume.number
        })
    return formated_volumes

# Get list of chapters information
def get_list_chapters(title):
    formated_chapters = []
    query_chapters = list(ChapterModel.objects.filter(volume__title__rus_name=title.rus_name))

    for chapter in query_chapters:
        increment_views(chapter)
        formated_chapters.append({
            "count": chapter.count,
            "content": chapter.content,
            "views": chapter.views,
            "likes": chapter.likes
        })
    return formated_chapters

