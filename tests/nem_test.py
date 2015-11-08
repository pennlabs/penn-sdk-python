import unittest
from penn import News, Map


class TestNEM(unittest.TestCase):

    def setUp(self):
        from credentials import NEM_USERNAME, NEM_PASSWORD
        username = NEM_USERNAME
        password = NEM_PASSWORD
        self.assertFalse(username is None or password is None)
        self.news = News(username, password)
        self.map = Map(username, password)

    def test_news(self):
        # News test times out
        # data = self.news.search("pennsylvania")
        # self.assertEquals(data['result_data'][0]['content_type'], 'news')
        pass

    def test_map(self):
        data = self.map.search("Towne")
        self.assertEquals(data['result_data'][0]['content_type'], 'map')
