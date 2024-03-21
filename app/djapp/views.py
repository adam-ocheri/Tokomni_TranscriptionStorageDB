from django.shortcuts import render
from django.db import connection
from django.db.models import Q
from .models import CallPart, ConversationItem, FullCallData
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ConversationItemSerializer, CallPartSerializer, FullCallDataSerializer
from .views_utils import util_get_conversation_item_view, util_get_call_part_view, util_get_full_calldata__view

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
        callparts = CallPart.objects.filter(fullcall_id=selected_call_id)
        # For each CallPart, fetch its related ConversationItems
        conversation_items = ConversationItem.objects.filter(callpart_id__in=selected_callpart_id)
        

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

# Create your views here.
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
            # Exclude 'speaker' and 'call_part' from being updated
            validated_data.pop('speaker', None)
            validated_data.pop('callpart_id', None)
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
