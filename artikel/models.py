from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Artikel(models.Model):
	judul 		= models.CharField(max_length=255)
	isi   		= models.TextField()
	kategori 	= models.CharField(max_length=255)
	published 	= models.DateTimeField(auto_now_add=True)
	updated 	= models.DateTimeField(auto_now=True)
	slug 		= models.SlugField(blank=True,editable=False)

	def save(self):
		self.slug = slugify(self.judul)
		super().save()

	def get_absolute_url(self):
		url_slug = {'slug':self.slug}
		return reverse('artikel:detail',kwargs = url_slug)
		# reverse == mengembalikan
		# get_absolute_url tujuan setelah createview di buat, dan reverse mengembalikan ke detail yang dimana url nya ada slug

	def __str__(self):
		return "{}.{}".format(self.id,self.judul)