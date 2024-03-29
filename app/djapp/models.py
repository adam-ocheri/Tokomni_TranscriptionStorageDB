from django.db import models
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField

# Create your models here.

class FullCallData(models.Model):
    id = models.UUIDField(primary_key=True, editable=True, auto_created=False)
    cdr_uuid = models.CharField(max_length=200) # editable=False
    domain = models.TextField(default="")
    epoch = models.BigIntegerField(default=0)


class CallPart(models.Model):
    id = models.UUIDField(primary_key=True, editable=True, auto_created=False)
    fullcall_id = models.ForeignKey(FullCallData, on_delete=models.CASCADE)
    file_location = models.TextField()
    extension = models.IntegerField(default=0)
    extension_uuid = models.CharField(max_length=200, default="") # editable=False
    status = models.IntegerField(default=0)
    engine_version = models.CharField(max_length=200, default="")
    user_id = models.UUIDField(editable=True, auto_created=False)


class ConversationItem(models.Model):
    text = models.TextField()
    speaker = models.CharField(max_length=20)
    search_vector = SearchVectorField(null=True, blank=True)
    timestamp = models.FloatField(default=0.0)
    callpart_id = models.ForeignKey(CallPart, on_delete=models.CASCADE, related_name='conversation_items')

    class Meta:
        indexes = [
            GinIndex(fields=['search_vector'])
        ]
