
from django.db.models import Model, TextField, IntegerField, ManyToManyField, ForeignKey, CASCADE

class TagModel(Model):
    name = TextField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'    
    
class TitleModel(Model):
    rus_name = TextField()
    eng_name = TextField(default='')
    other_name = TextField(default='')
    desc = TextField()
    tags = ManyToManyField(TagModel)

    def __str__(self) -> str:
        return self.rus_name

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

class VolumeModel(Model):
    title = ForeignKey(TitleModel, on_delete=CASCADE)
    name = TextField()
    cost = IntegerField()
    number = IntegerField()

    def __str__(self) -> str:
        return self.title.rus_name

    class Meta:
        verbose_name = 'Том'
        verbose_name_plural = 'Томы'

class ChapterModel(Model):
    volume = ForeignKey(VolumeModel, on_delete=CASCADE)
    count = IntegerField()
    content = TextField()
    views = IntegerField(default=0)
    likes = IntegerField(default=0)

    def __str__(self) -> str:
        return self.volume.title.rus_name

    class Meta:
        verbose_name = 'Глава'
        verbose_name_plural = 'Главы'