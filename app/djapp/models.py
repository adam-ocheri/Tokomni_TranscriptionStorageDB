from django.db import models
import uuid
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField

# Create your models here.
class DBItem(models.Model):
    pass

class FullCallData(models.Model):
    cdr_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    callog_uuid = models.UUIDField(default=uuid.uuid4, editable=True)
    extension = models.IntegerField()

class CallPart(models.Model):
    # id = models.UUIDField(default=uuid.uuid4, editable=False)
    # cdr_uuid = models.ForeignKey(FullCallData, on_delete=models.CASCADE)
    callog_uuid = models.ForeignKey(FullCallData, on_delete=models.CASCADE)
    file_location = models.TextField()


class ConversationItem(models.Model):
    # id = models.UUIDField(default=uuid.uuid4, editable=False)
    text = models.TextField()
    speaker = models.CharField(max_length=20)
    search_vector = SearchVectorField(null=True, blank=True)
    timestamp = models.FloatField(default=0.0)
    call_part = models.ForeignKey(CallPart, on_delete=models.CASCADE, related_name='conversation_items')

    class Meta:
        indexes = [
            GinIndex(fields=['search_vector'])
        ]