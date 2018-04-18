from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request, "index.html")

def login_action(request):
    if request.method == "POST":
        username1 = request.POST.get("username", "")
        password1 = request.POST.get("password", "")
        user = auth.authenticate(username=username1, password=password1)
        if user is not None:
            auth.login(request, user) #登陆
            response = HttpResponseRedirect("/event_manage/")
            #response.set_cookie("user", username, 3600)#添加浏览器cookie
            request.session['user_session'] = username1#将session信息记录到浏览器
            return response
        else:
            return render(request, "index.html", {"error": "username or password error!"})

#发布会管理
@login_required()
def event_manage(request):
    #username = request.COOKIES.get("user", "")
    username = request.session.get("user_session", "")#读取浏览器session
    return render(request, "event_manage.html", {"user": username})