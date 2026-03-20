from django.db import models
from django.conf import settings

class Dataset(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='datasets')
    name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    columns_json = models.TextField(blank=True, null=True)
    num_rows = models.IntegerField(default=0)
    blueprint_json = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} uploaded by {self.user.username}"
