from django.http import JsonResponse
from sign.models import Event
from django.core.exceptions import ValidationError,ObjectDoesNotExist

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
    if eid==''and name=='':
        return JsonResponse({'status':10021,'message':'pareameter error'})
    if eid!='':
        event=()
        try:
            result=Event.object.get(id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status':10022,'message':'queryresultisempty'})
        else:
            event['name']=result.name
            event['limit']=result.limit
            event['status']=result.status
            event['address'] = result.address
            event['start_time'] = result.start_time
            return JsonResponse({'status': 200, 'message': 'success', 'data': event})
    if name!='':
        datas=[]
        result=Event.objects.filter(name__contains=name)
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






