import re

from django.db import models
from django.db.utils import IntegrityError
from django.template.defaultfilters import stringfilter

from pages.models import Page
from versionutils import versioning, diff
from django.utils.html import strip_tags


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(editable=False, unique=True, max_length=100)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = strip_tags(self.name)
        self.slug = slugify(self.name)
        if not self.slug:
            raise IntegrityError('Invalid tag name: %s' % self.name)
        super(Tag, self).save(*args, **kwargs)

versioning.register(Tag)


def slugify(value):
    # normalize unicode
    import unicodedata
    value = unicodedata.normalize('NFKD', unicode(value))
    # remove non-word characters
    misc_characters = re.compile(('[^\w]'), re.UNICODE)
    value = re.sub(misc_characters, '', value)
    return value.lower()
slugify = stringfilter(slugify)


class PageTagSet(models.Model):
    page = models.OneToOneField(Page)
    tags = models.ManyToManyField(Tag)

    def __unicode__(self):
        return ', '.join(map(unicode, self.tags.all()))


class TagsFieldDiff(diff.BaseFieldDiff):
    template = 'tags/tags_diff.html'


class PageTagSetDiff(diff.BaseModelDiff):
    fields = (('tags', TagsFieldDiff),
              )


diff.register(PageTagSet, PageTagSetDiff)
versioning.register(PageTagSet)


import feeds  # To fire register() calls.
