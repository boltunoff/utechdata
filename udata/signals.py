from .models import SearchDataModel
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=SearchDataModel)
def index_post(sender, instance, **kwargs):
    instance.indexing()
