from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post, Category
from django.contrib.auth.models import User

class TestView(TestCase):
    def setUp(self):
        self.client=Client()
        self.user_kim = User.objects.create_user(
            username='kim',
            password='somepassword',
        )
        self.user_park = User.objects.create_user(
            username='park',
            password='somepassword',
        )

        self.category_programming = Category.objects.create(
            name='programming',
            slug='programming',
        )
        self.category_game = Category.objects.create(
            name='game',
            slug='game',
        )

        self.post_001 = Post.objects.create(
            title = 'First Post',
            content = 'Hello World',
            author = self.user_kim,
            category = self.category_programming,

        )
        self.post_002 = Post.objects.create(
            title = 'Project Sekai, Hatsune Miku',
            content = 'ようこそ、セカイへ',
            author = self.user_park,
            category = self.category_game,

        )
        self.post_003 = Post.objects.create(
            title = 'This Post has no category',
            content = 'No Category',
            author = self.user_park,
        )
        
    def category_card_test(self,soup):
        """Categories Widget Test"""
        cateries_card=soup.find('div', id='categories-card')
        self.assertIn('Categories', cateries_card.text)
        self.assertIn(f'{self.category_programming.name}({self.category_programming.post_set.count()})',cateries_card.text), 
        self.assertIn(f'{self.category_game.name}({self.category_game.post_set.count()})',cateries_card.text), 
        self.assertIn(f'未分類(1)', cateries_card.text)   

    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        about_me_btn = navbar.find('a', text='About Me')
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')

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
        
        main_area = soup.find('div', id='main-area')

        ## There are two post
        
        #3.2 Two Post Title exist in the Main Area
        #3.3 'There's no post yet' doesn't appear
        self.assertEqual(Post.objects.count(), 3)
        print("3 posts check")
        self.assertEqual(Post.objects.first().title, 'First Post')

        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content,'html.parser')

        self.assertEqual(response.status_code, 200)
        print('success :200')
        self.navbar_test(soup)
        self.category_card_test(soup)

        main_area = soup.find('div', id='main-area')
        post_001 = main_area.find('div', id='post-1')
        self.assertIn(self.post_001.title, post_001.text)
        self.assertIn(self.post_001.category.name, post_001.text)
        post_002 = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002.text)
        self.assertIn(self.post_002.category.name, post_002.text)
        #post_003 = main_area.find('div', id='post-3')
        #self.assertIn(self.post_003.title, post_003.text)
        #self.assertIn('未分類', post_003.text)
       
        
        self.assertIn(self.user_kim.username.upper(), main_area.text)
        self.assertIn(self.user_park.username.upper(), main_area.text)

        #self.assertNotIn('no post yet', main_area.text)

        #no post
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(),0)
        reponse=self.client.get('/blog/')
        soup=BeautifulSoup(response.content, 'html.parser')
        main_area=soup.find('div', id='main-area')
       

    def test_post_detail(self):
        #url /blog/1
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1')
        #response
        response = self.client.get(self.post_001.get_absolute_url())
        #200
        self.assertEqual(response.status_code, 200)
        #soup
        soup = BeautifulSoup(response.content, 'html.parser')
        #navbar
        self.navbar_test(soup)
        #category_card
        self.category_card_test(soup)
        #main_area
        main_area=soup.find('div', id='main-area')
        #post_area
        post_area=soup.find('div', id='post-area')
        #title
        self.assertIn(post_area.title, post_area.text)
        #category
        self.assertIn(self.category_programming.name, post_area.text)

        self.assertIn(self.user_kim.username.upper(), post_area.text)
        self.assertIn(self.post_001.content, post_area.text)

    def test_create_post(self):
        #Not Log In
        response = self.client.get('/blog/create_post')
        self.assertNotEqual(response.status_code, 200)

        #Log IN
        self.client.login(username='kim',password='somepassword')
        response=self.client.get('/blog/create_post')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        self.assertEqual('Create Post - Blog',soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Create New Post', main_area.text)

        self.client.post(
            '/blog/create_post/',
            {
                'title' : 'Create Post Form',
                'content' : 'Post Form page 生成',
            }
        )
        self.assertEqul(Post.objects.count(),4)
        last_post = Post.objects.last()
        self.assertEqual(last_post.title,'Create Post Form')
        self.assertEqual(last_post.author.username,'kim')
        
        self.assertEqual(last_post.content,'Post Form page 生成')
        
        

        


    
    

