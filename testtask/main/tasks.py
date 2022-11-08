def increment_views(chapter):
    chapter.views += 1
    chapter.save()

def increment_likes(chapter):
    chapter.likes += 1
    chapter.save()