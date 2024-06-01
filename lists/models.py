from django.db import models
from django.urls import reverse
from django.conf import settings

# Create your models here.
class List(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        blank=True, null=True
    )

    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])

    @property
    def name(self) -> str:
        return self.item_set.first().text

    @staticmethod
    def create_new(first_item_text, owner=None):
        list_ = List.objects.create(owner=owner)
        Item.objects.create(text=first_item_text, list=list_)
        return list_

class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, on_delete=models.CASCADE, default=None)

    class Meta:
        unique_together = ('list', 'text')
