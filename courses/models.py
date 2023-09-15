from django.db import models
from django.db.models import Avg
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from courses.fields import OrderField
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils import timezone
from autoslug import AutoSlugField

import numpy as np

class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

