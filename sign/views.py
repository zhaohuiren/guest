from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib import  auth
from django.contrib.auth.decorators import login_required
from sign.models import Event,Guest
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render,get_object_or_404
from django.core.exceptions import ValidationError,ObjectDoesNotExist
import logging
import requests
from addict import Dict
logger=logging.getLogger(__name__)
# Create your views here.
def index(request):
    return render(request,"index.html")


#登陆请求
def login_action(request):
    if request.method=='POST':#POST必须大写   得到客户发送的请求方式
        username=request.POST.get('username', '') #get方法来寻找页面中的name信息
        password=request.POST.get('password', '')
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)

            #response.set_cookie('user',username,3600)#添加浏览器cookie
            request.session['user']=username #将session信息记录到浏览器
            response = HttpResponseRedirect('/event_manage/')
            return  response
        else:
            return render(request,'index.html',{'error':'error'})


#发布会管理
@login_required()
def event_manage(request):
    #username=request.COOKIES.get('user','') #读取浏览器COOKIE
    event_list=Event.objects.all()
    username=request.session.get('user','') #读取浏览器seess
    weather = weater()
    return render(request, "event_manage.html", {"user": username,"events":event_list,'weather':weather})



#名称搜索
@login_required()
def search_name(request):
    username=request.session.get('user','')
    search_name=request.GET.get('name','')
    event_list=Event.objects.filter(name__contains=search_name)

    return  render(request,"event_manage.html",{"user":username,"events":event_list})



#嘉宾管理
@login_required()
def guest_manage(request):
    username=request.session.get('user','')
    guest_list= Guest.objects.all()
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts=paginator.page(page)
    except PageNotAnInteger:
        contacts=paginator.page(1)
    except EmptyPage:
        contacts=paginator.page(paginator.num_pages)



    return render(request,"guest_manage.html",{"user":username,"guests":contacts})


#签到界面
@login_required()
def sign_index(requsest,event_id):
    event=get_object_or_404(Event,id=event_id)
    return render(requsest,'sign_index.html',{'event':event})


#签到动作
@login_required
def sign_index_action(request,event_id):
    event=get_object_or_404(Event,id=event_id)
    phone=request.POST.get('phone','')
    result=Guest.objects.filter(phone=phone)
    if not result:
        return  render(request,'sign_index.html',{'event':event,'hint':'phone error'})
    result=Guest.objects.filter(phone=phone,event_id=event_id)
    if not  result:
        return  render(request,'sign_index.html',{'event':event,'hint':'event id or phone error'})
    result=Guest.objects.get(phone=phone,event_id=event_id)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event, 'hint': "user has sign in."})
    else:
        Guest.objects.filter(phone=phone,event_id=event_id).update(sign='1')
        return render(request,'sign_index.html',{'event':event,'hint':'sign in succerss','guest':result})




#退出登录
@login_required
def logout(request):
    auth.logout(request)#退出登陆
    response=HttpResponseRedirect('/index/')
    return response


@login_required
def add_event(request):
    return render(request,'add_event.html')



#添加发布会动作
@login_required
def add_event_action(request):
    if request.method=='POST':
        name=request.POST.get('name','')
        limit=request.POST.get('limit','')
        address=request.POST.get('address','')
        start_time=request.POST.get('start_time','')
        status=request.POST.get("status",'')
        if name==''or limit==''or address==''or start_time=='':
            return render(request,'add_event.html',{'error':'不能为空'})


        result = Event.objects.filter(name=name)
        if result:

            return  render(request,'add_event.html',{'error':'不能相同'})
        if status=='':
            status=1

        try:
            Event.objects.create(name=name, limit=limit, address=address, start_time=start_time, status=status)
        except ValidationError as e:
            return render(request,'add_event.html',{'error':'时间格式有问题'})



    return  render(request,'add_succers.html')


#添加成功
def add_event_success(request):
    return render(request,"add_succers.html")





#获取天气


def weater():
    r=requests.get('https://free-api.heweather.com/s6/weather/forecast?location=北京&key=4e6ea60db7634f3ba31616c733500301')
    a = r.json()
    dictionary = Dict(a)
    cond_txt_d = dictionary.HeWeather6[0].daily_forecast[0].cond_txt_d
    tmp_max = dictionary.HeWeather6[0].daily_forecast[0].tmp_max
    tmp_min = dictionary.HeWeather6[0].daily_forecast[0].tmp_min
    tmp=tmp_max+'C°-'+tmp_min+'C°'

    weater=cond_txt_d+' '+tmp
    return weater
