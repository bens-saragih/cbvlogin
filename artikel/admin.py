from django.contrib import admin

# Register your models here.
from .models import Artikel


# berguna untuk hanya bisa di baca saja
class ArtikelAdmin(admin.ModelAdmin):
	readonly_fields=[
						'slug',
						'updated',
						'published',
						
					]



admin.site.register(Artikel, ArtikelAdmin)