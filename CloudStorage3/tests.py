from django.contrib.auth import login
from django.test import TestCase, Client

# Create your tests here.
from CloudStorage3.models import User, Folder


def generate_random_name():
    return


class StorageTestCase(TestCase):

    def set_Up(self):
        self.client = Client()

    # def test_register(self):
    #     data = {'username': 'user3', 'password': '789', "confirmation": "789", "email": "user3@mail.com"}
    #     self.client.post('/register/', data=data)
    #     user = User.objects.get(username=data['username'])
    #     self.assertTrue(user)
    #
    #     user2 = User.objects.create_superuser(username="admin", password="123")
    #     self.assertEqual(user2.username, 'admin')
    #
    # def test_register_pass_no_match(self):
    #     data = {'username': 'user3', 'password': '789', "confirmation": '987', "email": "user3@mail.com"}
    #     res = self.client.post('/register/', data=data, follow=True)
    #     self.assertEqual(res.context.get('message'), 'Passwords must match.')
    #     user = User.objects.filter(username=data['username'])
    #     self.assertFalse(user)
    #
    # def test_login(self):
    #     user = User.objects.create(username="user4", password="1234")
    #     self.client.post('', data={"username": "user3", "password": "789"})
    #     self.assertTrue(user.is_authenticated)
    #
    # def test_create_dirs(self):
    #     user = User.objects.create(username="user4", password="1234")
    #     self.client.force_login(user=user)
    #     self.assertTrue(user.is_authenticated)
    #     self.client.post('/create_dir', data={"new_dir_name": "Dir_name1", 'current_dir_webpath': 'None'})
    #     self.assertTrue(Folder.objects.all())
    #     self.assertTrue(Folder.objects.first().name, "Dir_name1")
    #
    #     for i in range(2, 100):  # ]:->
    #         self.client.post('/create_dir', data={"new_dir_name": f"Dir_name{i}", 'current_dir_webpath': 'None'})
    #         self.assertEqual(Folder.objects.get(name=f"Dir_name{i}").name, f"Dir_name{i}")

    # def test_create_subdirs(self):
    #     user = User.objects.create(username="user4", password="1234")
    #     self.client.force_login(user=user)
    #     self.client.post('/create_dir', data={"new_dir_name": "Dir_name1", 'current_dir_webpath': 'None'})
    #
    #     sub_dir_names = ['Sub_Dir1', 'Sub_Dir2', 'Sub_Dir3', 'Sub_Dir4', 'Sub_Dir5']
    #
    #     current_dir_webpath = 'Dir_name1'
    #
    #     for sub_dir in sub_dir_names:
    #         self.client.post('/create_dir', data={"new_dir_name": sub_dir,
    #                                               'current_dir_webpath': current_dir_webpath})
    #         current_dir_webpath += '/' + sub_dir
    #
    #     sub_dir_objects = Folder.objects.filter(name__startswith='Sub').order_by('name')
    #
    #     for i, sub_dir in enumerate(sub_dir_names):
    #         self.assertEqual(sub_dir_objects[i].name, sub_dir)
