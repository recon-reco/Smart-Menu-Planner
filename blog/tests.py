from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

class TestView(TestCase):
    def setUp(self):
        self.client=Client()

    def navbar_test(self, soup):
        navbar=soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

    def test_post_list(self):
        ## Post List 仕組み　test
        #1.1 Get Post List page
        #1.2 Load Post List page
        #1.3 Title is 'Blog'
        #1.4 NavBar exists
        #1.5 Blog, About Me in NavBar
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code,200) 
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')
        
        self.navbar_test(soup)

        ## There is no post
        self.assertEqual(Post.objects.count(), 0)
        main_area = soup.find('div', id='main-area')
        self.assertIn("no post yet", main_area.text)

        ## There are two post
        post_001 = Post.objects.create(
            title = 'First Post',
            content = 'Hello World',
        )
        post_002 = Post.objects.create(
            title = 'Project Sekai, Hatsune Miku',
            content = 'ようこそ、セカイへ',
        )
        #3.2 Two Post Title exist in the Main Area
        #3.3 'There's no post yet' doesn't appear
        self.assertEqual(Post.objects.count(), 2)
        print("2 posts check")
        self.assertEqual(Post.objects.first().title, 'First Post')

        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content,'html.parser')

        self.assertEqual(response.status_code, 200)
        print('success :200')
        self.navbar_test(soup)
        main_area = soup.find('div', id='main-area')
        print(main_area.text)
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)

        self.assertNotIn('no post yet', main_area.text)


