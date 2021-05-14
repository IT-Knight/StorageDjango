from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError
from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.conf import settings

# Create your views here.
from CloudStorage3.models import User, StorageData, Folder, File, ActionLog

STORAGE_BASE_DIR = settings.BASE_DIR / settings.MEDIA_ROOT


class FileManager(View):

    def post(self, request):
        current_dir_webpath = request.POST['current_dir_webpath']
        if current_dir_webpath == 'None':  # Null from database goes into 'None' on render
            current_dir_webpath = None
        print('current_dir_webpath: ', current_dir_webpath, type(current_dir_webpath))
        post_files = request.FILES.getlist('files')
        print(post_files)
        user = get_object_or_404(User, id=request.user.id)
        username = request.user.username

        for file in post_files:
            value = file.size
            if value < 512000:
                value = value / 1024.0
                ext = 'Kb'
            elif value < 4194304000:
                value = value / 1048576.0
                ext = 'Mb'
            else:
                value = value / 1073741824.0
                ext = 'Gb'

            if not current_dir_webpath:
                parent_folder_name = request.user.username
                parent_folder_webpath = '/'
                file_webpath = '/' + file.name
            else:
                file_webpath = '/' + current_dir_webpath + '/' + file.name
                parent_folder_webpath = '/' + current_dir_webpath
                if '/' not in current_dir_webpath:
                    parent_folder_name = current_dir_webpath
                else:
                    parent_folder_name = current_dir_webpath.split('/')[-1]

            print('filename: ', file.name)
            print('file_webpath: ', file_webpath)
            print('parent_folder_name: ', parent_folder_name)
            print('parent_folder_webpath: ', parent_folder_webpath)

            size = '{0} {1}'.format(str(round(value, 2)), ext)

            data_object = StorageData(name=file.name, type='file', size=size,
                                      parent_folder_webpath=parent_folder_webpath, webpath=file_webpath, owner=user)

            # check if root_dir objects exists for user and create if not
            try:
                StorageData.objects.get(name=username, type='folder', parent_folder_webpath=None, webpath='/',
                                        owner=user)
            except StorageData.DoesNotExist:
                root_folder_data = StorageData.objects.create(name=username, type='folder', parent_folder_webpath=None,
                                                              webpath='/', owner=user)
                Folder.objects.create(name=username, webpath='/', data=root_folder_data).save()

            parent_folder_dataobj = StorageData.objects.get(owner=user, webpath=parent_folder_webpath)
            parent_folder_obj = Folder.objects.get(name=parent_folder_name, webpath=parent_folder_webpath, data=parent_folder_dataobj)
            try:
                data_object.save()
            except IntegrityError:  # if file exists - better to rewrite.
                continue

            File(data=data_object, file=file, parent_folder=parent_folder_obj).save()

            log_string = f'Uploaded file "{file.name}" ( {size} )'
            ActionLog(account=user, log_string=log_string, parent_folder=parent_folder_obj).save()

        print(current_dir_webpath)

        if current_dir_webpath is None:
            return redirect('main')
        else:
            return redirect('submain', dir_webpath=current_dir_webpath)


def download(request, data_id):
    data_obj = StorageData.objects.get(id=data_id)
    file_obj = File.objects.get(data=data_obj)
    filepath = file_obj.file.path
    print(filepath)
    response = FileResponse(open(filepath, 'rb'))
    print(response)
    print(response.filename)
    print(response.headers)
    return response


class MainInterfaceView(View):

    def get(self, request, dir_webpath=None):

        user = get_object_or_404(User, id=request.user.id)  # That's like @login_required, returns 404 not found

        print('dir_webpath', type(dir_webpath), dir_webpath)
        if not dir_webpath:
            extra_path = ''
            back_dir_path = None
            parent_dir_webpath = '/'
            parent_folder_name = request.user.username
        else:
            extra_path = dir_webpath + '/'
            parent_dir_webpath = '/' + dir_webpath
            if '/' not in dir_webpath:
                back_dir_path = '/main'
                parent_folder_name = dir_webpath
            else:
                back_dir_path = '/main/' + "/".join(dir_webpath.split('/')[:-1])
                parent_folder_name = dir_webpath.split('/')[-1]

            if len(extra_path) > 25:
                extra_path = extra_path[:25] + '..'

        print('parent_dir_name:', parent_folder_name)
        print('parent_dir_webpath:', parent_dir_webpath)
        print('back_dir_path', back_dir_path)
        print('extra_path: ', extra_path)

        user_folders_and_files = list(StorageData.objects.filter(owner=user, type="folder", parent_folder_webpath=parent_dir_webpath).order_by('name'))
        user_files = list(StorageData.objects.filter(owner=user, type="file", parent_folder_webpath=parent_dir_webpath).order_by('name'))
        user_folders_and_files += user_files

        for obj in user_folders_and_files:
            if obj.type == 'folder':
                obj.webpath = obj.webpath.lstrip('/')
            if len(obj.name) > 40:
                obj.showname = obj.name[:38] + '...'
            else:
                obj.showname = obj.name
        print(user_folders_and_files)

        action_logs = None

        if user_folders_and_files:
            parent_folder_dataobject = StorageData.objects.get(owner=user,
                                                               type="folder",
                                                               webpath=parent_dir_webpath,
                                                               name=parent_folder_name)

            parent_folder_obj = Folder.objects.get(name=parent_folder_name,
                                                   data=parent_folder_dataobject,
                                                   webpath=parent_dir_webpath)

            action_logs = ActionLog.objects.filter(account=user, parent_folder=parent_folder_obj).order_by('date')
        print('Action logs:', action_logs)

        return render(request, 'main.html', context={'folders_and_files': user_folders_and_files,
                                                     'current_dir_webpath': dir_webpath,
                                                     'back_dir': back_dir_path,
                                                     'extra_path': extra_path,
                                                     'action_logs': action_logs,
                                                     })


def delete_logs(request, webpath):
    user = get_object_or_404(User, id=request.user.id)

    if webpath == 'None':
        webpath = None

    if not webpath:
        parent_dir_webpath = '/'
        parent_folder_name = request.user.username
    else:
        parent_dir_webpath = '/' + webpath
        if '/' not in webpath:
            parent_folder_name = webpath
        else:
            parent_folder_name = dir_webpath.split('/')[-1]

    parent_folder_dataobject = StorageData.objects.get(owner=user, type="folder", webpath=parent_dir_webpath,
                                                       name=parent_folder_name)

    parent_folder_obj = Folder.objects.get(name=parent_folder_name, data=parent_folder_dataobject,
                                           webpath=parent_dir_webpath)

    ActionLog.objects.filter(account=user, parent_folder=parent_folder_obj).delete()
    print('Deleted')
    return HttpResponse(status=204)


def delete(request, data_id):
    print(data_id)
    user = get_object_or_404(User, id=request.user.id)
    obj = StorageData.objects.get(id=data_id)

    current_dir_webpath = obj.parent_folder_webpath

    if not current_dir_webpath or current_dir_webpath == '/':
        parent_folder_name = request.user.username
        parent_folder_webpath = '/'
    else:
        parent_folder_webpath = current_dir_webpath
        if '/' not in current_dir_webpath:
            parent_folder_name = current_dir_webpath
        else:
            parent_folder_name = current_dir_webpath.split('/')[-1]

    print(current_dir_webpath)
    print('parent_dir_name:', parent_folder_name)
    print('parent_dir_webpath:', parent_folder_webpath)

    parent_folder_dataobj = StorageData.objects.get(owner=user, webpath=parent_folder_webpath, type="folder")
    parent_folder_obj = Folder.objects.get(name=parent_folder_name, webpath=parent_folder_webpath,
                                           data=parent_folder_dataobj)

    log_string = f'Deleted {obj.type} "{obj.webpath}"'
    obj.delete()
    ActionLog.objects.create(account=user, log_string=log_string, parent_folder=parent_folder_obj)

    return HttpResponse(status=204)


class FolderManager(View):

    def post(self, request):
        data = request.POST

        current_dir_webpath = data['current_dir_webpath']
        if current_dir_webpath == 'None':  # why str type?! - that means Null from database goes into 'None' on render
            current_dir_webpath = None
        new_dir_name = data['new_dir_name']  # set_dir_name

        user = get_object_or_404(User, id=request.user.id)
        username = request.user.username

        # request.path  # /create_dir
        print('current_dir_webpath: ', current_dir_webpath, type(current_dir_webpath))

        if not current_dir_webpath:
            parent_folder_name = request.user.username
            parent_folder_webpath = '/'
            new_webpath = '/' + new_dir_name
        else:
            new_webpath = '/' + current_dir_webpath + '/' + new_dir_name
            parent_folder_webpath = '/' + current_dir_webpath
            if '/' not in current_dir_webpath:
                parent_folder_name = current_dir_webpath
            else:
                parent_folder_name = current_dir_webpath.split('/')[-1]

        print('new_webpath', new_webpath)
        print('parent_folder_name: ', parent_folder_name)
        print('parent_folder_webpath: ', parent_folder_webpath)

        data_object = StorageData(name=new_dir_name, type='folder', parent_folder_webpath=parent_folder_webpath, webpath=new_webpath, owner=user)


        # check if root_dir objects exists for user and create if not
        try:
            StorageData.objects.get(name=username, type='folder', parent_folder_webpath=None, webpath='/', owner=user)
        except StorageData.DoesNotExist:
            root_folder_data = StorageData.objects.create(name=username, type='folder', parent_folder_webpath=None, webpath='/', owner=user)
            Folder.objects.create(name=username, webpath='/', data=root_folder_data).save()

        parent_folder_dataobj = StorageData.objects.get(owner=user, webpath=parent_folder_webpath)
        parent_folder_obj = Folder.objects.get(name=parent_folder_name, webpath=parent_folder_webpath, data=parent_folder_dataobj)

        data_object.save()
        Folder(name=new_dir_name, webpath=new_webpath, data=data_object, parent_folder=parent_folder_obj).save()

        log_string = f'Created directory "{new_dir_name}"'
        ActionLog(account=user, log_string=log_string, parent_folder=parent_folder_obj).save()

        print(current_dir_webpath)

        if current_dir_webpath is None:
            return redirect('main')
        else:
            return redirect('submain', dir_webpath=current_dir_webpath)

    def patch(self, request):
        data = request.PATCH
        return


class Register(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('main')
        else:
            return render(request, 'register.html')

    def post(self, request):
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()

        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect('home')


def login_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('main')
        else:
            return render(request, "login.html")

    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:  # is not None:
            login(request, user)
            return redirect("main")
        else:
            return render(request, "login.html", {
                "message": "Invalid credentials."
            })


def logout_view(request):
    logout(request)
    return redirect('home')