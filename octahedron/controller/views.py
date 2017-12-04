from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from django.http import HttpResponse,JsonResponse
from django.urls import reverse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
import re, os, sys, zipfile, time

from controller.operation import ssh_execute,BatchExecute, preExecute
# Create your views here.
from django.views.decorators.http import require_POST,require_GET

from .models import *

def index(request):
    hosts = Host.objects.all()
    modules = Modules.objects.all()
    context = {'hosts':hosts, 'modules':modules}
    return render(request, 'controller/index.html', context)


def host_manage(request):
    context = {}
    return render(request, 'controller/host_manage.html', context)

@require_POST
def add_host_submit(request):
    ip = request.POST['ip']
    user = request.POST['username']
    password = request.POST['passwd']
    sshd = ssh_execute.ssh_execute(ip, user, password)
    if sshd.client:
        Host.objects.create(host_ip=request.POST['ip'], host_user=request.POST['username'], host_password=request.POST['passwd'])
    return HttpResponseRedirect(reverse('controller:index')) #提交完成后跳转回index

@require_POST
@csrf_exempt
def remove_host(request):
    ip = request.POST['ip']
    try:
        host = Host.objects.get(host_ip=ip)
        host.delete()
    except:
        pass
    return HttpResponseRedirect(reverse('controller:index'))  # 提交完成后跳转回index

@csrf_exempt
@require_POST
def check_host(request):
    if not request.is_ajax():
        return ;
    ip = request.POST['ip']
    user = request.POST['username']
    password = request.POST['passwd']
    sshd = ssh_execute.ssh_execute(ip, user, password)
    if sshd.client:
        text = 'Success'
    else:
        text = 'failed to connect host, please check!'
    return HttpResponse(text)

def module_manage(request):
    context = {}
    return render(request, 'controller/module_manage.html', context)

@require_POST
def add_module_submit(request):
    modulename = request.POST['module_name']
    onceonly = request.POST['isOnceonly']
    description = request.POST['description']
    Modules.objects.create(module_name=modulename, module_onceonly=onceonly, module_description=description)
    return HttpResponseRedirect(reverse('controller:index'))

@csrf_exempt
@require_POST
def remove_module(request):
    modulename = request.POST['module_name']
    try:
        module1 = Modules.objects.get(module_name=modulename)
        module1.delete()
    except:
        pass
    return HttpResponseRedirect(reverse('controller:index'))

@require_POST
@csrf_exempt
def save_config(request):
    f = open(sys.path[0]+"/controller/static/controller/modules/"+request.POST["module"]+"/module.html", "r")
    html = f.readlines()
    f.close()
    conf = open(sys.path[0]+"/controller/static/controller/modules/"+request.POST["module"]+"/module.conf", "w",newline='\n')
    f = open(sys.path[0]+"/controller/static/controller/modules/"+request.POST["module"]+"/module.html", "w")
    pattern = 'value=".*?"'
    patt = ' name=".*?" '
    for line in html:
        if line.find("<input ") != -1:
            if re.search(patt, line):
                s = re.search(patt, line).group()
                name = s[7:-2]
                if name in request.POST:
                    line = re.sub(pattern, 'value="'+request.POST[name]+'"', line)
                    conf.write("export "+name+"="+request.POST[name]+"\n")
        f.write(line)

    f.close()
    conf.close()
    return HttpResponse("Success")

#start_task 负责创建task任务并且将任务的id返回
@csrf_exempt
@require_POST
def start_task(request):
    if "modules[]" not in request.POST or "hosts[]" not in request.POST:
        return HttpResponse("failed")
    path = os.getcwd() + "/controller/static/controller/modules/";
    filename = os.getcwd() + "/controller/static/controller/module.zip"
    zip(path, filename)
    modules = request.POST.getlist("modules[]")
    hosts = request.POST.getlist("hosts[]")
    task = Task.objects.create()
    for host in hosts:
        task.hosts.add(Host.objects.get(host_ip=host))
    for m in modules:
        task.modules.add(Modules.objects.get(module_name=m))
    return HttpResponse(task.id)

def HTMLEditor(request):
    context = {}
    return render(request, 'controller/HTMLEditor.html', context)

def FileEditor(request):
    context = {}
    return render(request, 'controller/FileEditor.html', context)

# 在HTMLEditor或者FileEditor 中选择打开文件时, 将文件读出并返回给前台
@csrf_exempt
@require_POST
def openfile(request):
    if "filepath" not in request.POST:
        return HttpResponse("empty filepath", status=550);
    filepath = request.POST["filepath"]
    if ".." in filepath or "\\" in filepath:
        return HttpResponse("bad filepath!", status=550)
    path = os.getcwd()+"/controller/static/" + filepath
    if not os.path.isfile(path):
        return HttpResponse("not such file!", status=550)
    with open(path, "r") as file:
        string = file.read()
    return HttpResponse(string, status=200)

#在fileEditor或者HTMLEditor中, 提交文件并保存到后台
@csrf_exempt
@require_POST
def submitFile(request):
    if "filepath" not in request.POST or "TestCode" not in request.POST:
        return HttpResponse("filepath or Code is Empty!", status=550);
    filepath = request.POST["filepath"]
    code = request.POST["TestCode"]
    if ".." in filepath or "\\" in filepath:
        return HttpResponse("bad filepath!", status=550)
    path = os.getcwd() + "/controller/static/" + filepath
    pathdir = path[:path.rindex("/")]
    if not os.path.exists(pathdir):
        os.makedirs(pathdir)
    with open(path, "w") as file:
        file.write(code)
    return HttpResponse("success", status=200)

#zip负责打包modules
def zip(path, filename):
    try:
        import zlib
        compression = zipfile.ZIP_DEFLATED
    except:
        compression = zipfile.ZIP_STORED
    z = zipfile.ZipFile(filename, mode = "w",compression = compression)
    start = len(path)
    try:
        for dirpath, dirs, files in os.walk(path):
            for file in files:
                if file == filename:
                    continue
                #print(file)
                z_path = os.path.join(dirpath, file)
                z.write(z_path, z_path[start:])
        z.close()
    except:
        try:
            z.close()
        except:
            pass



