from django import forms
from django.db import models

from versionutils.versioning.forms import CommentMixin
from pages.models import Page
from utils.static import static_url

from models import Tag


class TagsForm(CommentMixin, forms.Form): 
    terms = forms.CharField()
