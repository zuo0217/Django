from django.test import TestCase
from sign.models import Event, Guest
from django.contrib.auth.models import User


# Create your tests here.

class ModelTest(TestCase):
    def setUp(self):
        Event.objects.create(id=1, name="oneplus 3 event", status=True, limit=2000, address="shenzhen",
                             start_time="2018-04-15 10:18:47")
        Guest.objects.create(id=1, event_id=1, realname="saseny", phone="1314159265", email="saseny@163.com",
                             sign=True)

    def test_event_models(self):
        """
        单个函数验证: python3 manage.py test sign.tests.ModelTest.test_event_models"""
        result = Event.objects.get(name='oneplus 3 event')
        self.assertEqual(result.address, 'shenzhen')
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(phone="1314159265")
        self.assertEqual(result.realname, 'saseny')
        self.assertTrue(result.sign)


class IndexPageTest(TestCase):
    """测试index登录首页"""

    def test_index_page_renders_index_template(self):
        """测试index视图"""
        response = self.client.get('/index/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response)


class LoginActionTest(TestCase):
    def setUp(self):
        User.objects.create_user("admin", "admin@mail.com", "admin123456")

    def test_add_admin(self):
        """测试添加用户"""
        user = User.objects.get(username="admin")
        self.assertEqual(user.username, "admin")
        self.assertEqual(user.email, "admin@mail.com")

    def test_login_action_username_password_null(self):
        """用户名密码为空"""
        test_data = {"username": "", "password": ""}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)

    def test_login_action_username_password_error(self):
        """用户名密码错误"""
        test_data = {"username": "abc", "password": "123"}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)

    def test_login_action_success(self):
        """登录成功"""
        test_data = {"username": "admin", "password": "admin123456"}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 302)


class EventManageTest(TestCase):
    """发布会管理"""

    def setUp(self):
        User.objects.create_user("admin", "admin@mail.com", "admin123456")
        Event.objects.create(name="xiaomi5", limit=2000, address="beijing", status=1, start_time="2018-04-15 10:18:47")
        self.login_user = {"username": "admin", "password": "admin123456"}

    def test_event_manage_success(self):
        """测试发布会: xiaomi5"""
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/event_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"xiaomi5", response.content)
        self.assertIn(b"beijing", response.content)

    def test_event_manage_search_success(self):
        """测试发布会搜索"""
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/search_name/', {"name": "xiaomi5"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"xiaomi5", response.content)
        self.assertIn(b"beijing", response.content)


class GuestManageTest(TestCase):
    """嘉宾管理"""

    def setUp(self):
        User.objects.create_user("admin", "admin@mail.com", "admin123456")
        Event.objects.create(id=1, name="xiaomi5", limit=2000, address="beijing", status=1,
                             start_time="2018-04-15 10:18:47")
        Guest.objects.create(realname="saseny", phone="15216857991", email="saseny@mail.com", sign=0, event_id=1)
        self.login_user = {"username": "admin", "password": "admin123456"}

    def test_guest_manage_success(self):
        """测试嘉宾信息"""
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/guest_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"saseny", response.content)
        self.assertIn(b"15216857991", response.content)

    def test_guest_manage_search_success(self):
        """测试嘉宾搜索"""
        response = self.client.post("/login_action/", data=self.login_user)
        response = self.client.post("/search_phone/", {"phone": "15216857991"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"saseny", response.content)
        self.assertIn(b"15216857991", response.content)


class SignIndexActionTest(TestCase):
    """发布会签到"""

    def setUp(self):
        User.objects.create_user("admin", "admin@mail.com", "admin123456")
        Event.objects.create(id=1, name="xiaomi5", limit=2000, address="beijing", status=1,
                             start_time="2018-04-19 10:18:47")
        Event.objects.create(id=2, name="oneplus4", limit=2000, address="shenzhen", status=1,
                             start_time="2018-04-18 10:20:47")
        Guest.objects.create(realname="alan", phone="13637390116", email="alan@mail.com", sign=0, event_id=1)
        Guest.objects.create(realname="saseny", phone="15216857991", email="saseny@mail.com", sign=1, event_id=2)
        self.login_user = {"username": "admin", "password": "admin123456"}

    def test_sign_index_action_phone_null(self):
        """手机号为空"""
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/1/', {"phone": ""})
        self.assertEqual(response.status_code, 200)
        self.assertIn("电话号码错误,请确认.".encode("utf-8"), response.content)

    def test_sign_index_action_phone_or_event_id_error(self):
        """手机号或发布会id错误"""
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/2/', {"phone": "13637390116"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("发布会场错误或电话号号码错误.".encode("utf-8"), response.content)

    def test_sign_index_action_user_sign_has(self):
        """用户已签到"""
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/2/', {"phone": "15216857991"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("已签到.".encode("utf-8"), response.content)

    def test_sign_index_action_sign_success(self):
        """签到成功"""
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/1/', {"phone": "13637390116"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("签到成功!".encode("utf-8"), response.content)
