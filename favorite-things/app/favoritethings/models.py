import uuid
from jsonfield import JSONField
from django.db import models
from django.utils.timezone import now

class Category(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=42)
    created_on = models.DateTimeField(default=now, blank=False)
    modify_on = models.DateTimeField(default=now, blank=False)
    def __str__(self):
        ret = self.title + '[' + str(self.uuid) + ']'
        return ret

class FavoriteThing(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=42)
    description = models.CharField(max_length=255)
    ranking = models.PositiveSmallIntegerField(default=1, null=False, blank=False)
    meta_data = JSONField(default={})
    category = models.ForeignKey(Category, related_name = "favoritethings", on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=now, blank=False)
    modify_on = models.DateTimeField(default=now, blank=False)
    def __str__(self):
        ret = self.title + '[' + str(self.uuid) + ']'
        return ret

class ThingHistory(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hist_index = models.PositiveSmallIntegerField(default=1, null=False, blank=False)
    favorties_things_connect = models.ForeignKey(FavoriteThing, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=now, blank=False)
    modify_on = models.DateTimeField(default=now, blank=False)
    hist_data = JSONField(default={})
    def __str__(self):
        ret = self.favorties_things_connect.title + '#' + str(self.hist_index) + '[' + str(self.uuid) + ']'
        return ret
