from base.models import Box
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views import View
from django.db.models import Q
from django.urls import reverse_lazy
import asyncio
import json
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from django import http
from create_box import handle_uploaded_box
from .models import Box, BoxService
from .forms import UploadFileForm 
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import classonlymethod, method_decorator
from django.http import JsonResponse

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('boxes')

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('boxes')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('boxes')
        return super(RegisterPage, self).get(*args, **kwargs)

@method_decorator(csrf_exempt, name="dispatch")
class Boxes(LoginRequiredMixin, ListView):
    model = Box
    context_object_name = 'boxes'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get('search') or ''
        if search_input:
            #context['boxes'] = context['boxes'].filter(boxservice__port=search_input) 
            context['boxes'] = context['boxes'].filter(Q(ip__icontains=search_input) | Q(hostname__icontains=search_input)) 
        context['search_input'] = search_input
        context['count'] = context['boxes'].count()
        context['services_count'] = BoxService.objects.count()
        return context

    #PASS NEW DATA
    def post(self, *args, **kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            new_box = Box.objects.filter(new=True)
            new_service = BoxService.objects.filter(new=True)
            body_unicode = self.request.body.decode('utf-8')
            body = json.loads(body_unicode)
            stat = None
            try:
                stat = str(body['stat'])
            except:
                pass
            if new_box or new_service:
                Box.objects.all().update(new=False)
                BoxService.objects.all().update(new=False)
                stat2 = {'stat':stat}
                stat2 = json.dumps(stat2)
                return JsonResponse(stat2, safe=False, status=200)
            else:
                return JsonResponse({"test":"test"}, status=400)
            #print(self.request.POST)

            #official_count = Box.objects.count()
            #data_count = body['count']
            #print(data_count)

class BoxDetail(LoginRequiredMixin, DetailView):
    model = Box
    context_object_name = 'box'
    template_name='base/box.html'
    '''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = BoxService.objects.filter(cBox='45.33.32.156')
        return context
    '''


class BoxCreate(LoginRequiredMixin, CreateView):
    model = Box
    context_object_name = 'box_form'
    fields = ['user', 'comments', 'active']
    success_url = reverse_lazy('boxes')

class BoxUpdate(LoginRequiredMixin, UpdateView):
    model = Box
    fields = ['user', 'comments', 'active', 'pwned']
    context_object_name='box_form'
    success_url = reverse_lazy('boxes')

#CHANGE THIS TO CLASS BASED
'''
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_box(request.FILES['file'])
            return HttpResponseRedirect('boxes')
    else:
        form = UploadFileForm()
    return render(request, 'base/upload.html', {'form': form})
'''

@method_decorator(csrf_exempt, name="dispatch")
class BoxUpload(View):
    def post(self, request, *args, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_box(request.FILES['file'])
        #handle_uploaded_box(request.POST)
            return redirect('boxes')
        else:
            handle_uploaded_box(request.FILES)
                
    def get(self, request, *args, **kwargs):
        form = UploadFileForm()
        return render(request, 'base/upload.html', {'form': form})