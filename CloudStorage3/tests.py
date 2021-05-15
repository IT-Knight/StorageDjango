import os
import shutil
import time

from django.contrib.auth import login
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.
from CloudStorage3.models import User, Folder, File, StorageData


class StorageTestCase(TestCase):

    def set_Up(self):
        self.client = Client()

    def test_register(self):
        data = {'username': 'user3', 'password': '789', "confirmation": "789", "email": "user3@mail.com"}
        self.client.post('/register/', data=data)
        user = User.objects.get(username=data['username'])
        self.assertTrue(user)

        user2 = User.objects.create_superuser(username="admin", password="123")
        self.assertEqual(user2.username, 'admin')

    def test_register_pass_no_match(self):
        data = {'username': 'user3', 'password': '789', "confirmation": '987', "email": "user3@mail.com"}
        res = self.client.post('/register/', data=data, follow=True)
        self.assertEqual(res.context.get('message'), 'Passwords must match.')
        user = User.objects.filter(username=data['username'])
        self.assertFalse(user)

    def test_login(self):
        user = User.objects.create(username="user4", password="1234")
        self.client.post('', data={"username": "user3", "password": "789"})
        self.assertTrue(user.is_authenticated)

    def test_create_dirs(self):
        user = User.objects.create(username="user4", password="1234")
        self.client.force_login(user=user)
        self.assertTrue(user.is_authenticated)
        self.client.post('/create_dir', data={"new_dir_name": "Dir_name1", 'current_dir_webpath': 'None'})
        self.assertTrue(Folder.objects.all())
        self.assertTrue(Folder.objects.first().name, "Dir_name1")

        for i in range(2, 100):
            self.client.post('/create_dir', data={"new_dir_name": f"Dir_name{i}", 'current_dir_webpath': 'None'})
            self.assertEqual(Folder.objects.get(name=f"Dir_name{i}").name, f"Dir_name{i}")

    def test_create_subdirs(self):
        user = User.objects.create(username="user4", password="1234")
        self.client.force_login(user=user)
        self.client.post('/create_dir', data={"new_dir_name": "Dir_name1", 'current_dir_webpath': 'None'})

        sub_dir_names = ['Sub_Dir1', 'Sub_Dir2', 'Sub_Dir3', 'Sub_Dir4', 'Sub_Dir5']

        current_dir_webpath = 'Dir_name1'

        for sub_dir in sub_dir_names:
            self.client.post('/create_dir', data={"new_dir_name": sub_dir,
                                                  'current_dir_webpath': current_dir_webpath})
            current_dir_webpath += '/' + sub_dir

        sub_dir_objects = Folder.objects.filter(name__startswith='Sub').order_by('name')

        for i, sub_dir in enumerate(sub_dir_names):
            self.assertEqual(sub_dir_objects[i].name, sub_dir)

    def test_upload_files(self):

        user = User.objects.create(username="user4", password="1234")
        self.client.force_login(user=user)

        dir_abs_path = os.getcwd()  # it's project's BASE_DIR, and not the app's
        base_relative_path1 = 'static\\image'

        dist_dir = os.path.join(dir_abs_path, base_relative_path1)

        fl_pre = os.listdir(dist_dir)

        file_list = [dist_dir + '\\' + x for x in os.listdir(dist_dir)]

        data = {}
        files = []

        for file in file_list:
            fp = open(file, 'rb')
            files.append(fp)

        data['files'] = files
        data['current_dir_webpath'] = 'None'

        self.client.post('/upload', data)

        res_files = [x.name for x in StorageData.objects.filter(owner=user, type="file")]

        self.assertEqual(len(file_list), File.objects.all().count())

        for file in fl_pre:
            self.assertIn(file, res_files)

        # Using django tests requires manual file delete, because no delete signals on receivers
        storage_dir = os.path.join(dir_abs_path, 'storage\\')
        shutil.rmtree(storage_dir + 'user4')

    def test_upload_to_subdir(self):
        user = User.objects.create(username="user4", password="1234")
        self.client.force_login(user=user)

        self.client.post('/create_dir', data={"new_dir_name": "Dir_name1", 'current_dir_webpath': 'None'})

        dir_abs_path = os.getcwd()
        base_relative_path1 = 'static\\image'
        dist_dir = os.path.join(dir_abs_path, base_relative_path1)
        fl_pre = os.listdir(dist_dir)
        file_list = [dist_dir + '\\' + x for x in os.listdir(dist_dir)]

        data = {}
        files = []

        for file in file_list:
            fp = open(file, 'rb')
            files.append(fp)

        data['files'] = files
        data['current_dir_webpath'] = 'Dir_name1'

        self.client.post('/upload', data)

        res_files_objects = StorageData.objects.filter(owner=user, type="file")
        res_files_names = [x.name for x in StorageData.objects.filter(owner=user, type="file")]

        self.assertEqual(len(file_list), File.objects.all().count())

        for file in fl_pre:
            self.assertIn(file, res_files_names)

        for obj in res_files_objects:
            self.assertEqual(obj.parent_folder_webpath, '/Dir_name1')

        storage_dir = os.path.join(dir_abs_path, 'storage\\')
        shutil.rmtree(storage_dir + 'user4')

    def test_download(self):
        user = User.objects.create(username="user4", password="1234")
        self.client.force_login(user=user)

        dir_abs_path = os.getcwd()
        base_relative_path1 = 'static\\image'

        dist_dir = os.path.join(dir_abs_path, base_relative_path1)

        fl_pre = os.listdir(dist_dir)

        file_list = [dist_dir + '\\' + x for x in os.listdir(dist_dir)]

        data = {}
        files = []

        for file in file_list:
            fp = open(file, 'rb')
            files.append(fp)

        data['files'] = files
        data['current_dir_webpath'] = 'None'

        self.client.post('/upload', data)

        for file in fl_pre:
            file_obj = StorageData.objects.get(name=file, type='file', owner=user)
            res = self.client.get('/download/' + str(file_obj.id))
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.headers['Content-Disposition'].split('; filename="')[-1].strip('"'), file_obj.name)
            res.close()

        storage_dir = os.path.join(dir_abs_path, 'storage\\')
        shutil.rmtree(storage_dir + 'user4')
