from django.shortcuts import render
from django.db import connection
from django.db.models import Q
from .models import CallPart, ConversationItem, FullCallData
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ConversationItemSerializer, CallPartSerializer, FullCallDataSerializer
from .views_utils import util_get_conversation_item_view, util_get_call_part_view, util_get_full_calldata__view
import uuid

def home(request):
    return render(request, "home.html")

def items(request):
    db_items = CallPart.objects.all()
    return render(request, "items.html", {"items": db_items})

def search(request):
    query = request.GET.get('search_query')
    # parent_fk = request.GET.get('parent_fk')
    selected_call_id = request.GET.get('selected_call_id')
    selected_callpart_id = request.GET.get('selected_callpart_id')
    # selected_callpart_id
    calls = FullCallData.objects.all()
    callparts = CallPart.objects.none()
    conversation_items = ConversationItem.objects.none()

    if selected_call_id:
        # Filter CallParts based on the selected FullCallData
        callparts = CallPart.objects.filter(fullcall_id=uuid.UUID(selected_call_id))
        # For each CallPart, fetch its related ConversationItems
    if selected_callpart_id:
        conversation_items = ConversationItem.objects.filter(callpart_id=uuid.UUID(selected_callpart_id))
        

    if query:
        conversation = conversation_items.filter(Q(speaker__search=query) | Q(text__search=query))
    else:
        conversation = conversation_items        

    context = {
        'items': conversation,
        'calls': calls,
        'callparts': callparts,
        'conversation_items': conversation_items,
    }

    list(conversation) # This is to trigger the query to be printed earlier due to Django ORM lazy loading

    print("Looking at QUERIES:")
    for query in connection.queries:
        print("--------------------")
        print(query)
        print("--------------------")
    # context = {'items': conversation, 'calls': calls, 'callparts': callparts}
    return render(request, 'main/index.html', context)

@api_view(['GET'])
def get_callparts_by_fullcall_id(request):
    query = request.GET.get('fullcall_id')
    domain = request.GET.get('domain')
    engine_version = request.GET.get('engine_version')
    extension = request.GET.get('extension')
    callparts = FullCallData.objects.none()

    if domain:
        fullcalls = FullCallData.objects.filter(domain__search=domain)
        domain_fullcall_ids = fullcalls.values_list('id', flat=True)
        callparts = CallPart.objects.filter(fullcall_id__in=domain_fullcall_ids)

    # if not engine_version and query:
    #     q = Q(fullcall_id=query)
    # elif engine_version:
    #     q = (Q(engine_version__search=engine_version))
    # elif query and engine_version:
    #     q = (Q(fullcall_id__search=query) | Q(engine_version__search=engine_version))
    # else:
    #     q = Q()
    
    q = Q()
    if query:
        q &= Q(fullcall_id=query)
    if engine_version:
        q &= (Q(engine_version__search=engine_version))

    # append queries to the QuerySet using &=
    if extension:
        q &= (Q(extension=int(extension)))
    
    if domain:
        callparts = callparts.filter(q)
    else:
        callparts = CallPart.objects.filter(q)

    result = []

    for callpart in callparts:
        conversation_items = ConversationItem.objects.filter(callpart_id=callpart.id)
        serializer = ConversationItemSerializer(conversation_items, many=True)
        result.append(serializer.data)
    
    return Response(result, status=200)

@api_view(['GET'])
def get_conversation_items_by_callpart(request):
    print("GET ConversationItems via CallPart_ID...")
    print(request)
    query = request.GET.get('callpart_id')
    search_vector = request.GET.get('search_vector')
    speaker = request.GET.get('speaker')
    print("QUERY: ", query)

    if query:
        try:
            callpart_id = uuid.UUID(query)  # Convert the string to a UUID object
        except ValueError:
            return Response({'error': 'Invalid UUID format'}, status=400)
        
        if query and not search_vector:
            q = Q(callpart_id=callpart_id)
        elif query and search_vector and not speaker:
            q = (Q(callpart_id=callpart_id) | Q(search_vector__search=search_vector))
        elif query and search_vector and not speaker:
            q = (Q(callpart_id=callpart_id) | Q(search_vector__search=search_vector))
        elif query and search_vector and speaker:
            q = (Q(callpart_id=callpart_id) 
                | Q(speaker__search=speaker) 
                | Q(search_vector__search=search_vector)
                )
        
        conversation_items = ConversationItem.objects.filter(q)
        serializer = ConversationItemSerializer(conversation_items, many=True)
        return Response(serializer.data, status=200)
    else:
        return Response("Missing query parameter \'callpart_id\' in request url", status=400)
    

@api_view(['POST'])
def store_new_transcription_job(request):
    data = request.data
    print("GOT DATA AFTER TRANSCRIPTION: ", data)
    # Deserialize FullCallData
    fullcall_serializer = FullCallDataSerializer(data=data.get("fullcalldata"))
    if fullcall_serializer.is_valid():
        fullcall_instance = fullcall_serializer.save()
    else:
        return Response(fullcall_serializer.errors, status=400)

    # Deserialize CallPart objects
    callpart_data = data.get("callpart")
    print("Printing Callpart: ", callpart_data)
    callpart_data["fullcall_id"] = str(fullcall_instance.id)  # Set the foreign key
    callpart_serializer = CallPartSerializer(data=callpart_data)
    if callpart_serializer.is_valid():
        callpart_instance = callpart_serializer.save()
    else:
        # Rollback the created FullCallData instance if any error occurs
        fullcall_instance.delete()
        return Response(callpart_serializer.errors, status=400)

    # Deserialize ConversationItem objects
    conversation_items_data = data.get("conversation_items", [])
    for conversation_item_data in conversation_items_data:
        conversation_item_data["callpart_id"] = str(callpart_instance.id)  # Set the foreign key
        conversation_item_serializer = ConversationItemSerializer(data=conversation_item_data)
        if conversation_item_serializer.is_valid():
            conversation_item_serializer.save()
        else:
            # Rollback the created FullCallData and CallPart instances if any error occurs
            fullcall_instance.delete()
            callpart_instance.delete()
            return Response(conversation_item_serializer.errors, status=400)

    return Response("Finished Job", status=201)

# View Classes
class ConversationItemView(APIView):
    def get(self, request):
        serializer = util_get_conversation_item_view(request)
        return Response(serializer.data)

    def post(self, request):
        serializer = ConversationItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def put(self, request, pk, format=None):
        try:
            item = ConversationItem.objects.get(pk=pk)
        except ConversationItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ConversationItemSerializer(item, data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            validated_data.pop('speaker', None) # Exclude 'speaker' from being updated
            validated_data.pop('callpart_id', None) # Exclude 'call_part' from being updated
            serializer.save(**validated_data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        try:
            item = ConversationItem.objects.get(pk=pk)
        except ConversationItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CallPartView(APIView):
    def get(self, request):
        serializer = util_get_call_part_view(request) 
        return Response(serializer.data)

    def post(self, request):
        serializer = CallPartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def put(self, request, pk, format=None):
        try:
            item = CallPart.objects.get(pk=pk)
        except CallPart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CallPartSerializer(item, data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            validated_data.pop('fullcall_id', None)
            serializer.save(**validated_data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        try:
            item = CallPart.objects.get(pk=pk)
        except CallPart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FullCallDataView(APIView):
    def get(self, request):
        serializer = util_get_full_calldata__view(request) 
        return Response(serializer.data)

    def post(self, request):
        serializer = FullCallDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def put(self, request, pk, format=None):
        try:
            item = FullCallData.objects.get(pk=pk)
        except FullCallData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = FullCallDataSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        try:
            item = FullCallData.objects.get(pk=pk)
        except FullCallData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
