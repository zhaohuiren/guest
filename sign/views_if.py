from django.http import JsonResponse
from sign.models import Event,Guest
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.db.utils import IntegrityError
import time

#添加发布会接口
def add_event(request):
    #通过post请求接受发布会的参数
    eid=request.POST.get('eid','')#发布会id
    name=request.POST.get('name','')#名称
    limit=request.POST.get('limit','')#限制人数
    status=request.POST.get('status','')#状态
    address=request.post.get('address','')#地址
    start_time=request.POST.get('start_time','')#发布会时间
    #首先判断不能为空
    if eid==''or name==''or limit==''or address=='' or start_time=='':
        return JsonResponse({'status':10021,'message':'parameter error'})

    result=Event.objects.filter(id=eid)

    if result:#判断id是否存在
        return JsonResponse({'status':10022,'message':'event id already exists'})


    result=Event.objects.filter(name=name)
    if result:#判断名称是否存在
        return  JsonResponse({'stetus':10023,'message':'event name already exists'})
    if status=='':#判断状态是否没空 为空返回1
        status=1

    try:
        Event.objects.create(id=eid,name=name,limit=limit,address=address,status=int(status),start_time=start_time) #插入数据
    except ValidationError as e: #处理时间的异常
        error= 'start_time format error. It must be in YYYY-MM-DD HH:MM:SS format.'
        return JsonResponse({'status':10024,'message':error})
    return JsonResponse({'status':200,'message':'add event success'})#返回插入成功


#发布会查询接口
def get_event_list(request):
    eid=request.GET.get('eid','')  #发布会id
    name=request.GET.get('name','')#发布会名称

    #通过get请求接受参数
    if eid==''and name=='':
        #判断是否都为空 返回错误
        return JsonResponse({'status':10021,'message':'pareameter error'})
    if eid!='':
        #判断id不为空
        event={}
        try:
            result=Event.object.get(id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status':10022,'message':'queryresultisempty'})
        else:
            #，将查询结果以key: value对的方式存放到定义的event字典中，并将数据字典作为整个返回字典中data对应的值返回。
            event['name']=result.name
            event['limit']=result.limit
            event['status']=result.status
            event['address'] = result.address
            event['start_time'] = result.start_time
            return JsonResponse({'status': 200, 'message': 'success', 'data': event})
    if name!='':
        datas=[]
        result=Event.objects.filter(name__contains=name)
        #首先将查询的每一条数据放到一 个字典 event 中，再把每一个字典再放到数组 datas 中，最后再将整个数组做为返回字典中 data 对应的值返回
        if result:
            for r in result:
                event={}
                event['name']=r.name
                event['limit'] =r.limit
                event['status'] = r.status
                event['address'] = r.address
                event['start_time'] = r.start_time
                datas.append(event)
            return JsonResponse({'status':200,'message':'success','date':datas})
        else:
            return JsonResponse({'status':1002,'message':'queryresultisempty'})



#添加嘉宾接口
def add_guest(request):
    #通过POST请求接收嘉宾参数：关联的发布会id、姓名、手机号和邮箱等参数
    eid=request.POST.get('eid','')  #关联发布会id
    realname=request.POST.get('realname','')#姓名
    phone=request.POST.get('phone','')#电话
    email=request.POST.get('email','')#邮箱
    #判断 eid、realname、phone 等参数均不能为空
    if eid=='' or realname=='' or phone=='':
        return JsonResponse({'status':10021,'message':'parameter error'})
    #判断id是否存在
    result=Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({'status':10022,'message':'event id null'})
    #判断状态是否为true
    result=Event.objects.get(id=eid).status
    if not result:
        return JsonResponse({'status':10023,'message':'event status is not available'})
    #判断人数
    event_limit=Event.objects.get(id=eid).limit #发布会限制人数
    guest_limit=Guest.objects.filter(event_id=id) #发布会已添加嘉宾数
    if len(guest_limit)>=event_limit:
        return JsonResponse({'status':10024,'message':'event number is full'})

    event_time=Event.objects.get(id=eid).start_time #发布会时间
    etime=str(event_time).split(".")[0] #split Python split()通过指定分隔符对字符串进行切片，如果参数num 有指定值，则仅分隔 num 个子字符串
    timeArray=time.strptime(etime, "%Y-%m-%d %H:%M:%S")# strptime()方法分析表示根据格式的时间字符串。返回值是一个struct_time所返回gmtime()或localtime()。
    e_time=int(time.mktime(timeArray)) #.mktime返回用秒数来表示时间的浮点数。
    now_time=str(time.time())#当前时间
    ntime=now_time.split('.')[0]
    n_time=int(ntime)
    #判断时间
    if n_time>=e_time:
        return JsonResponse({'status': 10025, 'message': 'event has started'})
    try:
        Guest.objects.create(realname=realname,phone=int(phone),email=email,sign=0,event_time=id(eid))
    except IntegrityError: #外键重复一异常
        return JsonResponse({'status':10026,'message':'the event guest phone number repeat'})
    return JsonResponse({'status':200,'message':'add guest success'})


#嘉宾查询接口
def get_guest_list(request):
    eid=request.GET.get("eid","")  #关联发布会
    phone=request.GET.get("phone","")#嘉宾手机号

    if eid=='':
        return JsonResponse({'status':10021,'message':'eid cannot be empty'})
    if eid!='' and phone!='':
        datas=[]
        results=Guest.objects.filter(event_id=eid)
        if results:
            for r in results:
                guest={}
                guest['realname']=r.realname
                guest['phone']=r.phone
                guest['email']=r.email
                guest['sign']=r.sign
                datas.append(guest)
            return JsonResponse({'status':200,'message':'successs','data':'datas'})
        else:
            return JsonResponse({'status':10022,'message':'queryresultisempty'})


    if eid!=''and phone!='':
            guest={}
            try:
                result=Guest.objects.get(phone=phone,event_id=eid)
            except ObjectDoesNotExist:
                return  JsonResponse({'status':10022,'message':'queryresultisempty'})
            else:
                guest['realname']=result.realnme
                guest['phone']=result.phone
                guest['email']=result.email
                guest['sign']=result.sign
                return JsonResponse({'status':200, 'message':'success', 'data':guest})




#嘉宾签到接口

def uesr_sign(request):
    eid=request.POST.get('eid','') #发布会id
    phone=request.POST.get('phone','')#嘉宾手机号

    if eid=='' or phone=='':
        return JsonResponse({'status':10021,'message':'parameter error'})
    result=Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({'status':10022,'message':'event id null'})

    result=Event


