import os
import shutil
import uuid
from pathlib import Path

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.conf import settings


class ActionLog(models.Model):
    account = models.ForeignKey('User', on_delete=models.CASCADE)
    log_string = models.CharField(max_length=512)
    date = models.DateTimeField(auto_now_add=True)
    parent_folder = models.ForeignKey('Folder', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.account.username}: {self.log_string} ({self.parent_folder.webpath})"


# Create your models here.
def user_directory_path(instance, filename):

    path = instance.parent_folder.webpath
    if os.name == "nt":
        if path == "/":
            print('user_directory_path: {0}\{1}'.format(instance.data.owner.username, filename))
            return '{0}\{1}'.format(instance.data.owner.username, filename)
        else:
            path = path.replace('/', '\\')
            print('user_directory_path: {0}{1}\{2}'.format(instance.data.owner.username, path, filename))
            return '{0}{1}\{2}'.format(instance.data.owner.username, path, filename)
    elif os.name == "posix":
        if path == "/":
            print('user_directory_path: {0}/{1}'.format(instance.data.owner.username, filename))
            return '{0}/{1}'.format(instance.data.owner.username, filename)
        else:
            path = path.replace('\\', '/').replace('\\\\', '/')
            print('user_directory_path: {0}{1}/{2}'.format(instance.data.owner.username, path, filename))
            return '{0}{1}/{2}'.format(instance.data.owner.username, path, filename)


class File(models.Model):
    data = models.ForeignKey('StorageData', on_delete=models.CASCADE)
    parent_folder = models.ForeignKey('Folder', on_delete=models.CASCADE)
    file = models.FileField(blank=True, null=True, max_length=256, upload_to=user_directory_path)


@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """

    if instance.file:
        file_path = instance.file.path
        if os.path.isfile(file_path):
            print("Deleted:", file_path)
            os.remove(file_path)


@receiver(models.signals.pre_save, sender=File)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False
    try:
        old_file = StorageData.objects.get(pk=instance.pk).file
    except StorageData.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


class Folder(models.Model):
    data = models.ForeignKey('StorageData', on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    webpath = models.CharField(max_length=256, default='/')
    parent_folder = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __repr__(self):
        return 'Folder: {0} (Path: {1})'.format(self.name, self.webpath)


@receiver(models.signals.pre_delete, sender=Folder)
def auto_delete_folder_on_delete(sender, instance, **kwargs):
    if instance.webpath:

        dir_path = str(settings.BASE_DIR) + '\\' + instance.data.owner.username + '\\' + instance.webpath.lstrip('/').replace('/', '\\')
        if os.path.isdir(dir_path):
            if dir_path not in ('C:\\', 'C:\\Users\\'):  # broken pathlib returns 'C:\'
                shutil.rmtree(dir_path)
            else:
                assert f'BASE_DIR broken again! Folder delete path: {dir_path}'

            # Folder.objects.filter(dir_path__startswith=dir_path).delete()


class StorageData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    type = models.CharField(max_length=6)
    size = models.CharField(max_length=256, blank=True, null=True)
    parent_folder_webpath = models.CharField(max_length=256, blank=True, null=True)
    webpath = models.CharField(max_length=256)
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    modify_date = models.DateTimeField(auto_now_add=True)
    locked = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'StorageData'
        unique_together = ['owner', 'webpath']
        # ordering = ['type', 'name']

    def __repr__(self):
        return 'Data-{0} (Owner: {1}) {2}'.format(self.name, self.owner, self.webpath)

    def __str__(self):
        return 'Data-{0}: {1} ({2}) {3}'.format(self.type.capitalize(), self.name, self.owner, self.modify_date.strftime('%d.%m.%Y %H:%M'))


class User(AbstractUser):

    def __repr__(self):
        return f'User({self.username}, {self.email})'
