from django.http import JsonResponse
from sign.models import Event
from django.core.exceptions import ValidationError
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

    if result:
        return JsonResponse({'status':10022,'message':'event id already exists'})


    result=Event.objects.filter(name=name)
    if result:
        return  JsonResponse({'stetus':10023,'message':'event name already exists'})
    if status=='':
        status==1

    try:
        Event.objects.create(id=eid,name=name,limit=limit,address=address,status=int(status),start_time=start_time)
    except ValidationError as e:
        error= 'start_time format error. It must be in YYYY-MM-DD HH:MM:SS format.'
        return JsonResponse({'status':10024,'message':error})
    return JsonResponse({'status':200,'message':'add event success'})





