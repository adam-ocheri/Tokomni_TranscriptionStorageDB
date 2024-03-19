from django.contrib import admin
from .models import ConversationItem, CallPart, FullCallData

# Register your models here.
admin.site.register(FullCallData)
admin.site.register(ConversationItem)
admin.site.register(CallPart)