from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
    event_list = Event.objects.all()
    #username = request.COOKIES.get("user", "")
    username = request.session.get("user_session", "")#读取浏览器session
    return render(request, "event_manage.html", {"user": username,
                                                 "events": event_list})

# 发布会名称搜索
@login_required()
def search_name(request):
    username = request.session.get("user_session", "")
    search_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"user": username, "events": event_list})

# 嘉宾管理
@login_required()
def guest_manage(request):
    username = request.session.get("user_session", "")
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 2)
    page = request.GET.get("page")
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果page不是整数，取第一页面的数据
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果page不在范围，取最后一页面
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username, "guests": contacts})

# 嘉宾搜索
@login_required()
def search_guestname(request):
    username = request.session.get("user_session", "")
    search_name = request.GET.get("guestname", "")
    guest_list = Guest.objects.filter(realname__contains=search_name)
    return render(request, "guest_manage.html", {"user": username, "guests": guest_list, "search_name":search_name})

# 签到页面
@login_required()
def sign_index(request, eid):
    event = get_object_or_404(Event, id=eid)
    return render(request, "sign_index.html", {"event": event})

# 签到动作
@login_required()
def sign_index_action(request,eid):
    event = get_object_or_404(Event, id=eid)
    guest_list = Guest.objects.filter(event_id=eid)
    sign_list = Guest.objects.filter(event_id=eid, sign='1')
    guest_num = str(len(guest_list))
    sign_num = str(len(sign_list))
    phone = request.POST.get('phone', '')
    print(phone)
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, "sign_index.html",{'event': event, "hint": "phone error.","sign":sign_num,"guest_total":guest_num})
    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        return render(request, "sign_index.html", {"event":event,"hint": "event id or phone error","sign":sign_num,"guest_total":guest_num})
    result = Guest.objects.get(phone=phone, event_id=eid)
    if result.sign:
        return render(request, "sign_index.html", {"event":event, "hint":"user has sign in","sign":sign_num,"guest_total":guest_num})
    else:
        Guest.objects.filter(phone=phone,event_id=eid).update(sign='1')
        return render(request, "sign_index.html",{"event":event,"hint":"sign in success!","guest":result,"sign":sign_num,"guest_total":str(int(guest_num)+1)})

# 退出
@login_required()
def logout(request):
    auth.logout(request) # 退出登录
    response = HttpResponseRedirect('/index/')
    return response