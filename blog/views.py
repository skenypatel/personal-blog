from django.shortcuts import render, get_object_or_404,redirect
from .models import Post
from django.utils import timezone
from .forms import PostForm
from django.template.defaultfilters import slugify
from .unique_slug import unique_slugify
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
	ListView, 
	DetailView,
	CreateView,
	UpdateView,
	DeleteView)
# Create your views here.
def home(request):
	context={
		'posts':Post.objects.all()
	}
	return render(request, 'blog/index.html',context)

def about(request):
	return render(request, 'blog/about.html')

class PostListView(ListView):
	model=Post
	template_name='blog/index.html' #<app>/<model>_<viewtype>.html
	context_object_name='posts'
	ordering= ['-date_posted']
	paginate_by = 5

class PostDetailView(DetailView):
	model=Post
	fields=['title', 'blog_data', 'slug']	

class PostCreateView(LoginRequiredMixin, CreateView):
	model=Post
	fields=['title','blog_data']
	#redirect_field_name='/login/'
	def form_valid(self,form):
		form.instance.author=self.request.user
		form.instance.slug=unique_slugify(form.instance, form.instance.title)
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model=Post
	fields=['title','blog_data']
	#redirect_field_name='/login/'
	def form_valid(self,form):
		form.instance.author=self.request.user
		return super().form_valid(form)

	def test_func(self):
		post=self.get_object()
		if self.request.user==post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model=Post
	success_url='/'
	def test_func(self):
		post=self.get_object()
		if self.request.user==post.author:
			return True
		return False

def error_404_view(request, exception):
    data = {"name": "What?"}
    return render(request,'blog/404.html', data)
