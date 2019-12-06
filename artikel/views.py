from django.shortcuts import render,redirect
from django.views.generic import ListView,DetailView,CreateView,DeleteView,UpdateView
from .models import Artikel 
from .forms import ArtikelForm
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import UserPassesTestMixin

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('artikel:login')
    else:
        form = UserCreationForm()
    return render(request, 'artikel/signup.html', {
        'form': form
    })

#@user_passes_test(lambda user: Group.objects.get(name='updatef') in user.groups.all(),)
class ArtikelUpdateView(UserPassesTestMixin,UpdateView):
	login_url= None
	form_class = ArtikelForm
	model = Artikel
	template_name = 'artikel/artikel_update.html'





#@user_passes_test(lambda user: Group.objects.get(name='penulisf') in user.groups.all(),login_url='/message/')
class ArtikelCreateView(UserPassesTestMixin,CreateView):
	form_class = ArtikelForm
	template_name = 'artikel/artikel_create.html'
	permission_denied_message = 'Salah' 
	def get_permission_denied_message(self):
	    """
	    Override this method to override the permission_denied_message attribute.
	    """
	    return self.permission_denied_message

#@user_passes_test(lambda user: Group.objects.get(name='deletef') in user.groups.all(),login_url='/message/')
class ArtikelDeleteView(DeleteView):
	model = Artikel
	template_name = "artikel/artikel_delete_confirmation.html"
	success_url = reverse_lazy('artikel:manage')

class ArtikelManageView(ListView):
	model = Artikel
	template_name = "artikel/artikel_manage.html"
	context_object_name = 'artikel_list'



class ArtikelPerKategori():
	model = Artikel 

	def get_latest_artikel_each_kategori(self):
		kategori_list = self.model.objects.values_list('kategori',flat=True).distinct()
		queryset = []# isi nya kosong

		for kategori in kategori_list: # untuk kategori di dalam kategori list 
			artikel = self.model.objects.filter(kategori=kategori).latest('published')#artikel sama dengan objects dari model yang difilter berdasarkan kategori yang terakhir di published
			queryset.append(artikel)# variabel queryset merupakan list dan di dalamnya di tambahkan varibael artikel

		return queryset





class ArtikelKategoriListView(ListView):
	model = Artikel
	template_name = "artikel/artikel_kategori_list.html"
	context_object_name = 'artikel_list'
	ordering = ['-published']
	paginate_by = 3

	def get_queryset(self):
		self.queryset = self.model.objects.filter(kategori=self.kwargs['kategori'])
		return super().get_queryset()

	def get_context_data(self,*args,**kwargs):
		kategori_list = self.model.objects.values_list('kategori',flat=True).distinct().exclude(kategori=self.kwargs['kategori'])# sehingga nanti yang muncul sisanya
		#distinct berguna agar kategori yang di tamplikan tidak double
		# model adalah artikel uda di buat di atas, flat adalah untuk membuat list dan isi nya true
		self.kwargs.update({'kategori_list':kategori_list})
		kwargs = self.kwargs
		return super().get_context_data(*args,**kwargs)



class ArtikelListView(ListView):
	model = Artikel 
	template_name = 'artikel/artikel_list.html'
	context_object_name = 'artikel_list'# pengganti objects_list,atau di sebuat object name
	ordering = ['-published']
	paginate_by = 3

	def get_context_data(self,*args,**kwargs):
		kategori_list = self.model.objects.values_list('kategori',flat=True).distinct()
		#distinct berguna agar kategori yang di tamplikan tidak double
		# model adalah artikel uda di buat di atas, flat adalah untuk membuat list dan isi nya true
		self.kwargs.update({'kategori_list':kategori_list})
		kwargs = self.kwargs
		return super().get_context_data(*args,**kwargs)

class ArtikelDetailView(DetailView):
	model = Artikel
	template_name = 'artikel/artikel_detail.html'
	context_object_name = 'artikel'

	def get_context_data(self,*args,**kwargs):
		kategori_list = self.model.objects.values_list('kategori',flat=True).distinct()
		#distinct berguna agar kategori yang di tamplikan tidak double
		# model adalah artikel uda di buat di atas, flat adalah untuk membuat list dan isi nya true
		self.kwargs.update({'kategori_list':kategori_list})

		artikel_serupa = self.model.objects.filter(kategori=self.object.kategori).exclude(id=self.object.id)
		self.kwargs.update({'artikel_serupa':artikel_serupa})
		kwargs = self.kwargs
		return super().get_context_data(*args,**kwargs)