from django.db import models

class Section(models.Model):
    address = models.TextField()
    content = models.TextField()
    is_chapter = models.BooleanField()
    is_rule = models.BooleanField()
