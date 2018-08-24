from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic import View, ListView, DetailView, TemplateView
from django.conf import settings
from .models import Blog, Entry

# Create your views here.


class Index(TemplateView):

    template_name = 'telegram_blog/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['blogs'] = Blog.objects.all()
        return ctx


class WebhookView(View):
    def get(self):
        pass


class BlogListView(ListView):

    model = Blog
    template_name = 'telegram_blog/blog_list.html'

class BlogDetailView(DetailView):

    model = Blog
    template_name = 'telegram_blog/blog_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['entries'] = Entry.objects.filter(
            blog=self.object,
        ).order_by('-message_time')
        return ctx