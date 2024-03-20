
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ConversationItem

@receiver(post_save, sender=ConversationItem)
def update_search_vector(sender, instance : ConversationItem, **kwargs):
    print("SearchVector POST-SAVE CALLBACK!:\n   update_search_vector(sender, instance : ConversationItem, **kwargs)...\n")
    
    update_fields = kwargs.get('update_fields')
    if update_fields is None or 'search_vector' not in update_fields:
        instance.search_vector = instance.text + " " + instance.speaker
        instance.save(update_fields=['search_vector'])