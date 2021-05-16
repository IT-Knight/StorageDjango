## CloudStorage

**Why this project satisfies the distinctiveness?**

-There wasn't any "Cloud-storage with UI"-like projects before in course.

**Why do i believe this project satisfies the complexity requirements?**
 - First of all it's complexed by the main tasks for project: to find out by my self the theme for project different from before, and to make the application mobile-responsive.
 - Next, it implements a "file n' folder manager". You can create directories, navigate through them, upload files, see you action logs on each directory, and you can delete and download the content. 
 - So, it's tricky to develop a "folder manager". And wasn't any file-work before. The physical storage is path-organized and handles both Windows and Linux path-types.
 - After delete - files and folders by the right way physically got removed from the hard-drive storage, that doesn't  automatically implemented by django.
 - It has a drag-n-drop field for files upload using JS.
 - It's has an action log for user actions by directory, can be cleared.
 - It's handles overflow moments for the list of user's files and dirs, on pre-showing the files before upload, and in action logs,.
 - It has better design.
 - It contains django tests. Not absolute, only for basic functionality(listed below).
 - It's scalable to "lock", "rename", "copy" and "move" operations. Just like the OS filesystem. For thumbnails for image-type files. And even to collaboration system for many users on one storage. (i see it so).


**What’s contained in each file you created.**

I left the structure standard and easy.
```
- CloudStorage3/ - the main and only app of project
 |- admin.py 
 |- apps.py
 |- models.py
 |- tests.py
 |- urls.py
 |- views.py
- config/ - the main project's folder
 |-asgi.py
 |-settings.py
 |-urls.py 
 |-wsgi.py
- storage/ - django will auto-create this folder on first file upload operation.
 |- some_user1/ - the main-root folder for each user
   |- sub_folder1/
   |- sub-folder_n/
 |- some_user2/
- static/ - global "static" folder
 |- image/ - contains all the images for project
 |- login.css
 |- register.css
 |- main.css
 |- main.js
- templates/ - global templates folder
 |- login.html
 |- register.html
 |- main.html
- manage.py
- README.MD
- requirements.txt
- .gitignore - ignore python cache, pycharm's .idea/, Pipfile-s, and app/migrations/.

admin.py - register models for admin panel.
models.py - contains 5 models and 3 signal receivers for File and Folder models.
urls.py - contains all the web-paths
views.py - contains all the views
tests.py - contains some basic tests:
class StorageTestCase(TestCase):
 - test_register
 - test_register_pass_no_match
 - test_login
 - test_create_dirs
 - test_create_subdirs
 - test_upload_files
 - test_upload_to_subdir
 - test_download
 - test_delete
 - test_clear_log

```
**How to run your application.**
```
- Install django module, version 3.2.2 was used.
- Run "python3 manage.py makemigrations CloudStorage3"
- next "python3 manage.py migrate"
- "python3 manage.py runserver"
- register or create super-user
- login
```

**Any other additional information the staff should know about your project.**
The project was first developed and tested on Windows 10 on Google Chrome, where the front-end seemed well.
In Firefox it has a really little bug of coloring the background. That's because of unpredictable behavior of imported bootstrap. In Chrome it's well.
The app tested also on Linux Ubuntu 20.04 on Firefox - it goes like on Windows.
Mobile-responsability was tested by browser-emulator of device.
It doesn't has size control for uploaded files, so it's depends on free local memory. Big files can be uploaded too, but there's no progress bar, so maybe some waiting can be needed. I had 1 GB uploaded around a minute.

Finally, i'd like to say that the project is far from perfect(it can have endless improvements), but should be good anough for last cs50 Web project.