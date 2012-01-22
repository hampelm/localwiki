from django import forms
from django.db import models

from versionutils.versioning.forms import CommentMixin
from pages.models import Page
from utils.static import static_url

from models import Tag


class TagForm(CommentMixin, forms.ModelForm):
    term = forms.CharField()

    class Meta:
        model = Tag
        exclude = ('slug', 'page')

    class Media:
        js = (
              static_url('js/jquery/jquery-1.7.min.js'),
              static_url('js/jquery/jquery-ui-1.8.16.custom.min.js'),
        )
