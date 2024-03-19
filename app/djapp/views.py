from django.shortcuts import render
from .models import CallPart, ConversationItem

def home(request):
    return render(request, "home.html")

def items(request):
    db_items = CallPart.objects.all()
    return render(request, "items.html", {"items": db_items})

def main(request):

    query = request.GET.get('query')

    if query:
        conversation = ConversationItem.objects.filter(speaker__search=query)
    else:
        conversation = ConversationItem.objects.all()        


    context = {'items': conversation}
    return render(request, 'main/index.html', context)

# Create your views here.
