from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render, render_to_response, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sitemaps import Sitemap
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Q
from blog.models import Blog
from polls.models import Question, Choice 
from blog.forms import BlogForm, ContactForm
import datetime

# Create your views here.
def view_homepage(request):
	posts_list = Blog.objects.all().order_by("-id")
	questions_polls = Question.objects.all()

	query = request.GET.get("q")
	if query:
		posts_list = posts_list.filter(
			Q(title__icontains=query) |
			Q(subtitle__icontains=query) |
			Q(author__icontains=query) |
			Q(article__icontains=query) |
			Q(tags__icontains=query) |
			Q(date_added__icontains=query)
			)
	paginator = Paginator(posts_list, 5)

	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)

	title = "Search here"
	context = {
		#'title': title,
		'posts': queryset,
		'questions_polls': questions_polls,
	}
	return render(request, 'blog/index.html', context)

def view_aboutpage(request):
	return render(request, 'blog/about.html', {})

def view_contactpage(request):
	contact_form = ContactForm(request.POST or None)
	if contact_form.is_valid():
		form_name_or_title = contact_form.cleaned_data.get("name_or_title")
		form_email_adress = contact_form.cleaned_data.get("email_adress")
		form_contact_message = contact_form.cleaned_data.get("contact_message")

		subject = form_name_or_title
		from_email = form_email_adress
		contact_message = form_contact_message

		send_mail(subject+" - "+from_email, contact_message, from_email,
		['filip.markoski45@gmail.com'], fail_silently=False)

		return render(request, 'blog/contact_sent.html', {})

	context = {
		"contact_form": contact_form,
	}
	return render(request, 'blog/contact.html', context)


def view_blogpost(request, slug=None):
	instance = get_object_or_404(Blog, slug=slug)
	# if instance.publish > timezone.now().date() or instance.draft:
	# 	if not request.user.is_staff or not request.user.is_superuser:
	# 		raise Http404
	#share_string = quote_plus(instance.content)
	context = {
		#"title": instance.title,
		"article": instance,
		#"share_string": share_string,
	}
	return render(request, "blog/post.html", context)

# def view_blogpost(request, blog_id):
# 	article = Blog.objects.get(pk=blog_id)
# 	return render(request, 'blog/post.html', {'article':article})


@login_required
def view_makepost(request):
	form = BlogForm(request.POST or None)
	
	if form.is_valid():
		instance = form.save(commit=False)
		#
		author = form.cleaned_data.get("author")
		article = form.cleaned_data['article']
		if not author:
			author = request.user.username
		instance.author = author
		#
		instance.save()
		#messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		'form': form,
	}
	return render(request, 'blog/makepost.html', context)

@login_required
def view_updatepost(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	#post = Blog.objects.get(pk=blog_id)
	#blog_id = blog_id - 1
	post_to_be_changed = get_object_or_404(Blog, slug=slug)
	form = BlogForm(request.POST or None, instance=post_to_be_changed)
	print(post_to_be_changed.title)
	
	if form.is_valid():
		post_to_be_changed = form.save(commit=False)
		#
		#
		post_to_be_changed.save()
		#messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
		return HttpResponseRedirect(post_to_be_changed.get_absolute_url())

	context = {
		'post_to_be_changed': post_to_be_changed,
		'form': form,
	}
	return render(request, 'blog/makepost.html', context)

@login_required
def view_deletepost(request, slug=None):
	post = get_object_or_404(Blog, slug=slug).delete()


	posts = Blog.objects.all()
	questions_polls = Question.objects.all()
	context = {
		'posts': posts,
		'questions_polls': questions_polls,
	}
	return render(request, 'blog/index.html', context)

def custom_404(request):
	response = render_to_response('blog/404.html', {}, context_instance=RequestContext(request))
	response.status_code = 404
	return response

def custom_500(request):
	response = render_to_response('blog/500.html', {}, context_instance=RequestContext(request))
	response.status_code = 500
	return response

class blog_sitemap(Sitemap):
	changefreq = "daily"
	priority = 1.0
	lastmod = datetime.datetime.now()
	def items(self):
		return Blog.objects.all()