## CloudStorage

**Why this project satisfies the distinctiveness?**

-There wasn't any "Cloud-storage with UI"-like projects before in course.

**Why do i believe this project stisfies the complexity requirements?**
 - First of all it's complexed by the main tasks for project: to find out by my self the theme for project different from before, and to make the application mobile-responsive.
 - Next, it implements a "file n' folder manager". You can create directories, navigate through them, upload files, see you action logs on each directory, and you can delete and download the content. 
 - So, it's tricky to develop a "folder manager". And wasn't any file-work before. The phisical storage is path-organized.
 - After delete - files and folders by the right way physically got removed from the hard-drive storage, that doesn't  automatically implemented by django.
 - It handles a kinda many micro-things of mobile-responsibility.
 - It has better design.
 - It's scalable to "lock", "rename", "copy" and "move" operations. Just like the OS filesystem. For thumbnails for image-type files. And even to collaboration system for many users on one storage. 


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
models.py - contains 5 models and 3 signal recievers for File and Folder models.
urls.py - contains all the web-paths
views.py - contains all the views
tests.py - contains some basic tests:
```
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

```
**How to run your application.**
```
Nothing unusual needed.
- Install django module, version 3.2.2 was used.
- Run the "python manage.py makemigrations"
- next "python manage.py migrate"
- "python manage.py runserver"
- register or create super-user
- login
```

**Any other additional information the staff should know about your project.**
The project was tested on Windows 10 and on Linux environment. 