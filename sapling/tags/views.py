from django.core.urlresolvers import reverse

from versionutils.versioning.views import UpdateView, DeleteView
from versionutils import diff
from utils.views import CreateObjectMixin, PermissionRequiredMixin
from django.views.generic import ListView
from pages.models import Page, slugify

from models import Tag
from forms import TagForm

class TagListView(ListView):
    context_object_name = "page_list"
    template_name = "pages/page_list.html"

    def get_queryset(self):
        return Tag.objects.filter(slug__exact=self.kwargs['term_slug'])

    def get_context_data(self, **kwargs):
        
        context = super(TagListView, self).get_context_data(**kwargs)
       
        context['term_slug'] = self.kwargs['term_slug']
        print "hey!"
        return context


class TagUpdateView(CreateObjectMixin,
        UpdateView):
    model = Tag
    form_class = TagForm

    def get_object(self):
        term_slug = self.kwargs.get('term_slug')
        page_slug = slugify(self.kwargs.get('slug'))
        page = Page.objects.get(slug=page_slug)
        tag = Tag.objects.filter(slug=term_slug, page=page)
        if tag:
            return tag[0]
        return Tag(page=page, term=term_slug)

    def get_context_data(self, **kwargs):
        context = super(TagUpdateView, self).get_context_data(**kwargs)
        p = Page.objects.filter(slug=self.object.page)
        if p:
            context['page'] = p[0]
        else:
            context['page'] = Page(slug=self.object.page,
                name=self.object.page)
        context['exists'] = Tag.objects.filter(term=self.object.term)
        return context

    def success_msg(self):
        # NOTE: This is eventually marked as safe when rendered in our
        # template.  So do *not* allow unescaped user input!
        return (
            '<div>Thank you for your changes. '
            
            # TODO 
           #  'You have added the tag <a href="%s">%s</a>.</div>'
           #  % (self.object.get_absolute_url(),
           #     self.object)
        )

    def get_success_url(self):
        return reverse('pages:show', args=[self.object.page])

    def create_object(self):
        page = Page.objects.filter(slug=slugify(self.kwargs['page']))
        return Tag(page=page)

   # def get_protected_objects(self):
   #     protected = []
   #     slug = slugify(self.kwargs['slug'])
   #
   #     page = Page.objects.filter(slug=page)
   #     if page:
   #         protected.append(page[0])
   #     tag = Tag.objects.filter(slug=slug)
   #     if tag:
   #         protected.append(tag[0])
   #
   #     return protected

    def permission_for_object(self, obj):
        # We want to tie the tag permissions to the Tag object
        # -and- the Page object that's associated with the Tag.
        # This is so that if, for instance, Page(name="Front Page") is
        # only editable by a certain group, creating a Tag from
        # "Front Page" to somewhere is similarly protected.
        if isinstance(obj, Tag):
            return 'tags.change_tagt'
        elif isinstance(obj, Page):
            return 'pages.change_page'


class TagDeleteView(DeleteView):
    model = Tag

    def get_object(self):
        page = slugify(self.kwargs.get('page'))
        return Tag.objects.get(page=page)

    def get_context_data(self, **kwargs):
        context = super(TagDeleteViews, self).get_context_data(**kwargs)
        p = Page.objects.filter(slug=self.object.page)
        if p:
            context['page'] = p[0]
        else:
            context['page'] = Page(slug=self.object.page,
                name=self.object.page)
        return context

    def success_msg(self):
        # NOTE: This is eventually marked as safe when rendered in our
        # template.  So do *not* allow unescaped user input!
        return (
            '<div>Thank you for your changes. '
            'The tag has been deleted from the page.</div>'
        )

    def get_success_url(self):
        return reverse('pages:show', args=[self.object.page])


class TagCompareView(diff.views.CompareView):
    model = Tag

    def get_object(self):
        return Tag(page=slugify(self.kwargs.get('paeg')))

    def get_context_data(self, **kwargs):
        context = super(TagCompareView, self).get_context_data(**kwargs)
        context['page'] = Page(slug=self.object.page,
            name=self.object.page)
        return context
