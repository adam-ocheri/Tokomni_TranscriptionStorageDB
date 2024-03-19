from django.shortcuts import render
from django.db import connection
from django.db.models import Q
from .models import CallPart, ConversationItem
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ConversationItemSerializer

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
        items = ConversationItem.objects.all()
        serializer = ConversationItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ConversationItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)