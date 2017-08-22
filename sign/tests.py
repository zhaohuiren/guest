from django.test import TestCase
from sign.models import Event,Guest
from django.test import Client
from django.contrib.auth.models import User

from datetime import  datetime
# Create your tests here.
class ModelTest(TestCase):
    def setUp(self):
        Event.objects.create(
            id=1,
            name='oneplus3 event',
            status=True,
            limit=200,
            address='shenzhen',
            start_time='2016-08-31 02:18:11',
        )
        Guest.objects.create(
            id=1,
            event_id=1,
            realname='alen',
            phone='13121641251',
            email='alen@mial.com',
            sign=False

        )

    def test_event_modles(self):
        result=Event.objects.get(name='oneplus3 event')
        self.assertEqual(result.address,"shenzhen")
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(phone='13121641251')
        self.assertEqual(result.realname, "alen")
        self.assertFalse(result.sign)
class IndexPageTest(TestCase):
    '''测试index登录首页 '''
    def test_index_page_renders_index_template(self):
        response=self.client.get('/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'index.html')


class LoginActionTesst(TestCase):
    '''测试登录函数'''
    def setUp(self):
        User.objects.create_user('admin','admin@mail.com','rzh110120999')
        #初始化调用User.objects.create_user()创建登录用户数据。
        #  Client()类提供的 get()和 post() 方法可以模式 GET/POST 请求。
        self.c=Client()

    def test_login_action_username_password_null(self):
        '''用户名密码为空'''
        test_data={'username':'','password':''}
        respones=self.c.post('/login_action/',data=test_data)
        self.assertEqual(respones.status_code,200)
        self.assertIn(b"error",respones.content)


    def test_login_action_uesname_password_error(self):
        '''用户名密码错误'''
        test_date={'username':'abc','password':'123'}
        respones=self.c.post('/login_action/',data=test_date)
        self.assertEqual(respones.status_code,200)
        self.assertIn(b"error",respones.content)


    def test_login_action_successs(self):
        '''登录成功'''
        test_data={'username':'admin','password':'rzh110120999'}
        response = self.c.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 302)

class EventManageTest(TestCase):
    '''发布会管理'''
    def setUp(self):
        Event.objects.create(id=2,
                             name='xiaomi',
                             limit=1000,
                             status=True,
                             address='beijing',
                             start_time=datetime(2016,12,15,10,59.39))
        self.c=Client()

    def test_event_manage_success(self):
        '''测试发布会'''
        response=self.c.post('/event_manage/')
        self.assertEqual(response.status_code,200)
        self.assertIn(b'xiaomi',response.content)
        self.assertIn(b'beijing',response.content)

