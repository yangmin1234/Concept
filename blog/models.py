from django.db import models
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse
from django.utils.text import slugify
import datetime
# Create your models here.
class Blog(models.Model):
	title = models.CharField(max_length=250, unique=True)
	subtitle = models.CharField(max_length=250, null = True, blank=True)
	date_added = models.DateTimeField(default=datetime.datetime.now())
	image = models.TextField(max_length=1000, null = True, blank=True)
	tags = models.TextField(max_length=500, null=True, blank=True)
	article = models.TextField(max_length=15000, null=True, blank=True)
	author = models.CharField(max_length=150, null=True, blank=True)
	slug =models.SlugField(unique=True)

	def get_absolute_url(self):
		return reverse("post", kwargs={"slug": self.slug})

	#def get_absolute_url(self):
	#	return "/blog/%i" % self.pk

def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Blog.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug

def pre_save_blog_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)
	# slug = slugify(instance.title)
	# exists = Blog.objects.filter(slug=slug).exists()
	# if exists:
	# 	slug = "%s-%s" %(slug, instance.id)
	# instance.slug = slug

pre_save.connect(pre_save_blog_receiver, sender=Blog)