from django.db import models
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse

from pages.models import Page, slugify
from versionutils import versioning

import exceptions


class Tag(models.Model):
    term = models.TextField(max_length=255)
    slug = models.SlugField(max_length=255)
    page = models.ForeignKey(Page)
    
    unique_together = ("term", "slug", "page")

    def __unicode__(self):
        return "%s" % (self.term)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.term)
        super(Tag, self).save(*args, **kwargs)

   # TODO
   # def get_absolute_url(self):
   #     return reverse('pages:show', args=[self.source])

versioning.register(Tag)

import feeds # To fire register() calls.
