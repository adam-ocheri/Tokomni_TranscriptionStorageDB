from .models import CallPart, ConversationItem, FullCallData
from .serializers import ConversationItemSerializer, CallPartSerializer, FullCallDataSerializer

def util_get_conversation_item_view(request):
    pk = request.query_params.get('pk')
    parent_fk = request.query_params.get('parent_fk')
    if pk:
        item = ConversationItem.objects.get(pk=pk)
        return ConversationItemSerializer(item) 
    elif parent_fk:
        item = ConversationItem.objects.filter(callpart_id=parent_fk)
        return ConversationItemSerializer(item, many=True)
    else:
        item = ConversationItem.objects  
        return ConversationItemSerializer(item, many=True)      

def util_get_call_part_view(request):
    pk = request.query_params.get('pk')
    parent_fk = request.query_params.get('parent_fk')
    callpart_id = request.query_params.get('callpart_id')
    ext = request.query_params.get('extension')
    ext_id = request.query_params.get('extension_uuid')
    if pk:
        item = CallPart.objects.get(pk=pk)
        return CallPartSerializer(item)
    elif parent_fk:
        item = CallPart.objects.filter(fullcall_id=parent_fk)
        return CallPartSerializer(item, many=True)
    elif callpart_id:
        item = CallPart.objects.get(callpart_uuid=callpart_id)
        return CallPartSerializer(item)
    elif ext:
        item = CallPart.objects.filter(extension=ext)
        return CallPartSerializer(item, many=True)
    elif ext_id:
        item = CallPart.objects.filter(extension_uuid=ext_id)
        return CallPartSerializer(item, many=True)
    else:
        item = CallPart.objects  
        return CallPartSerializer(item, many=True)  

def util_get_full_calldata__view(request):
    pk = request.query_params.get('pk')
    cdr = request.query_params.get('cdr_id')
    calllog = request.query_params.get('calllog_id')
    if pk:
        item = FullCallData.objects.get(pk=pk)
        return FullCallDataSerializer(item) 
    elif cdr:
        item = FullCallData.objects.get(cdr_uuid=cdr)
        return FullCallDataSerializer(item)
    elif calllog:
        item = FullCallData.objects.get(calllog_uuid=calllog)
        return FullCallDataSerializer(item)
    else:
        item = FullCallData.objects.all() 
        return FullCallDataSerializer(item, many=True)    