from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
# contenttype can be used to create generic relationships


# models.Manager is the base class for all managers
from store.models import Product


class TaggedItemManager(models.Manager):

    def get_for_object(self, object_type, object_id):
        content_type = ContentType.objects.get_for_model(object_type)
        query_set = TaggedItem.objects.filter(
            content_type=content_type,
            object_id=object_id,
        ).select_related('tag')
        return query_set


class Tag(models.Model):
    label = models.CharField(max_length=255)


class TaggedItem(models.Model):
    objects = TaggedItemManager()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
