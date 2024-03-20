from django.shortcuts import render
from django.db import connection
from django.db.models import Q
from .models import CallPart, ConversationItem
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ConversationItemSerializer, CallPartSerializer

def home(request):
    return render(request, "home.html")

def items(request):
    db_items = CallPart.objects.all()
    return render(request, "items.html", {"items": db_items})

def search(request):
    query = request.GET.get('search_query')

    if query:
        conversation = ConversationItem.objects.filter(Q(speaker__search=query) | Q(text__search=query))
    else:
        conversation = ConversationItem.objects.all()        

    list(conversation) # This is to trigger the query to be printed later due to Django ORM lazy loading

    print("Looking at QUERIES:")
    for query in connection.queries:
        print("--------------------")
        print(query)
        print("--------------------")
    context = {'items': conversation}
    return render(request, 'main/index.html', context)

# Create your views here.
class ConversationItemView(APIView):
    def get(self, request):
        pk = request.query_params.get('pk')
        parent_fk = request.query_params.get('parent_fk')
        if pk:
            item = ConversationItem.objects.get(pk=pk)
            serializer = ConversationItemSerializer(item) 
        elif parent_fk:
            item = ConversationItem.objects.filter(call_part=parent_fk)
            serializer = ConversationItemSerializer(item, many=True)
        else:
            item = ConversationItem.objects  
            serializer = ConversationItemSerializer(item, many=True)  
        return Response(serializer.data)
        # items = ConversationItem.objects.all().first()
        # serializer = ConversationItemSerializer(data=items)
        # try:
        #     if serializer.is_valid(raise_exception=True):
        #         print("I AM HERE!")
        #         data = serializer.data
        #         return Response(data)
        # except Exception as e:
        #     print(e)
        # if serializer.is_valid():
        #     return Response(serializer.errors, status=400)
        # else:
        #     return Response("Error with serialization of DB object at ConversationItemView::get", status=400)


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
            validated_data.pop('call_part', None)
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
        items = CallPart.objects.all()
        serializer = CallPartSerializer(items, many=True)
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
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        try:
            item = CallPart.objects.get(pk=pk)
        except CallPart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
