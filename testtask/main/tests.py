from django.test import TestCase
from django.test.client import RequestFactory
import json
from .models import *
from .views import *

# Create your tests here.
class ApiTest(TestCase):
    def setUp(self) -> None:
        TagModel.objects.create(
            name = 'Мечта'
        )

        TagModel.objects.create(
            name = 'Мечты'
        )

        TagModel.objects.create(
            name = 'Любовь'
        )

        TitleModel.objects.create(
            rus_name = 'Книга о мечтах',
            eng_name = 'Book about dreams',
            other_name = '',
            desc = 'Марафон мечт'
        ).tags.set([TagModel.objects.get(name='Мечта'), TagModel.objects.get(name='Мечты')])

        TitleModel.objects.create(
            rus_name = 'Книга о любви',
            eng_name = 'Book about love',
            other_name = '',
            desc = 'Марафон любви'
        ).tags.set([TagModel.objects.get(name='Любовь')])

        VolumeModel.objects.create(
            title = TitleModel.objects.get(rus_name='Книга о мечтах'),
            name = "Все о мечтах",
            cost = 22500,
            number = 140
        )

        ChapterModel.objects.create(
            volume = VolumeModel.objects.get(title__rus_name='Книга о мечтах'),
            count = 20,
            content = 'gsgsdgsdgfsg'
        )


    def test_title_api(self):
        factory = RequestFactory()
        request = factory.get('/api/titles')
        response = titles(request)
        data = json.loads(response.content)
        excepted_data = {
            'msg': '',
            'content': 
            [
                {
                    'rus_name': 'Книга о мечтах',
                    'eng_name': 'Book about dreams', 
                    'other_name': '', 
                    'desc': 'Марафон мечт', 
                    'tags': ['Мечта', 'Мечты']
                },
                {
                    'rus_name': 'Книга о любви',
                    'eng_name': 'Book about love', 
                    'other_name': '', 
                    'desc': 'Марафон любви', 
                    'tags': ['Любовь']
                }
            ]
        }

        data_equal = data['content'][1]['rus_name'] == excepted_data['content'][1]['rus_name']
        self.assertEqual(data_equal, True)

    def test_title_count_api(self):
        factory = RequestFactory()
        request = factory.get('/api/titles?count=1')
        response = titles(request)
        data = json.loads(response.content)
        excepted_data = {
            'msg': '',
            'content': 
            [
                {
                    'rus_name': 'Книга о мечтах',
                    'eng_name': 'Book about dreams', 
                    'other_name': '', 
                    'desc': 'Марафон мечт', 
                    'tags': ['Мечта', 'Мечты']
                },
            ]
        }

        data_equal = data['content'][0]['rus_name'] == excepted_data['content'][0]['rus_name'] 
        self.assertEqual(data_equal, True)

    def test_title_details_api(self):
        factory = RequestFactory()
        request = factory.get('/api/titles_details')
        response = titles_details(request)
        data = json.loads(response.content)
        

        expected_data = {
            'msg': '',
            'content': [
                {
                    'rus_name': 'Книга о мечтах', 
                    'eng_name': 'Book about dreams', 
                    'other_name': '', 
                    'desc': 'Марафон мечт', 
                    'tags': ['Мечта', 'Мечты'], 
                    'volumes': [
                        {
                            'name': 'Все о мечтах',
                            'cost': 22500, 
                            'number': 140
                        }
                    ], 
                    'chapters': [
                        {
                            'count': 20, 
                            'content': 'gsgsdgsdgfsg', 
                            'views': 1, 
                            'likes': 0
                        }
                    ]
                }, 
                {
                    'rus_name': 'Книга о любви', 
                    'eng_name': 'Book about love', 
                    'other_name': '', 
                    'desc': 'Марафон любви', 
                    'tags': ['Любовь'], 
                    'volumes': [], 
                    'chapters': []
                }
            ]
        }

        data_equal = data['content'][0]['rus_name'] == expected_data['content'][0]['rus_name']
        self.assertEqual(data_equal, True)

    def test_chapter_api(self):
        factory = RequestFactory()
        request = factory.get('/api/chapter?id=1')
        response = chapter(request)
        data = json.loads(response.content)
        expected_data = {
            'msg': '',
            'content': [
                {
                    'volume': 'Книга о мечтах',
                    'count': 20, 
                    'views': 0, 
                    'likes': 0, 
                    'content': 'gsgsdgsdgfsg'
                }
            ]
        }

        data_equal = data['content'][0]['volume'] == expected_data['content'][0]['volume']
        self.assertEqual(data_equal, True)

    def test_like_api(self):
        factory = RequestFactory()
        request = factory.get('/api/like_chapter?id=1')
        response = like_chapter(request)
        data = json.loads(response.content)
        expected_data = {
            'msg': '', 
            'content': [
                {
                    'volume': 'Книга о мечтах', 
                    'likes': 1
                }
            ]
        }

        data_equal = data['content'][0]['likes'] == expected_data['content'][0]['likes']
        self.assertEqual(data_equal, True)