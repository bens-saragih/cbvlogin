from django.conf.urls import url,include
from .views import (
	ArtikelListView,
	ArtikelDetailView,
	ArtikelKategoriListView,
	ArtikelCreateView,
	ArtikelManageView,
	ArtikelDeleteView,
	ArtikelUpdateView,
	signup
	)
from django.contrib.auth import views as auth_views

urlpatterns = [
	url(r'^signup/', signup,name='signup'),
	url(r'^accounts/password_change_done/$', auth_views.PasswordChangeDoneView.as_view(template_name='artikel/changepassdone.html')),
	url(r'^accounts/password_change/$', auth_views.PasswordChangeView.as_view(template_name='artikel/changepass.html',success_url='home')),
	url(r'^accounts/logout/$', auth_views.LogoutView.as_view(template_name='artikel/logout.html')),
	url(r'^accounts/login/$', auth_views.LoginView.as_view(template_name='artikel/login.html')),
    url(r'^accounts/',include('django.contrib.auth.urls')),
	url(r'^manage/update/(?P<pk>\d+)$',ArtikelUpdateView.as_view(),name='update'),
	url(r'^manage/delete/(?P<pk>\d+)$',ArtikelDeleteView.as_view(),name='delete'),
	url(r'^manage/$',ArtikelManageView.as_view(),name='manage'),
	url(r'^tambah/$',ArtikelCreateView.as_view(),name='create'),
	url(r'^kategori/(?P<kategori>[\w]+)/(?P<page>\d+)$',ArtikelKategoriListView.as_view(),name='category'),
	url(r'^detail/(?P<slug>[\w-]+)$',ArtikelDetailView.as_view(),name='detail'),
	url(r'^(?P<page>\d+)$',ArtikelListView.as_view(),name='list'),
]