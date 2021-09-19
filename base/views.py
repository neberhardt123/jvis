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
import os
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from django import http
from base.modules.create_box import handle_uploaded_box
from base.modules import diagram
from .models import Box, BoxService
from .forms import UploadFileForm 
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import classonlymethod, method_decorator
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.conf import settings

#pip install --upgrade pip
#install nmap
#install unzip, wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip unzip ngrok-stable-linux-amd64.zip
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


class Boxes(LoginRequiredMixin, ListView):
    model = Box
    context_object_name = 'boxes'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get('search') or ''
        if search_input:
            if 'port=' in search_input:
                port_string=search_input.split("port=",1)[1]
                port_int=int(port_string.strip())
                #ports=port_string.split(",")
                ##for port in ports:
                #    port = port.strip()
                #    port = int(port)
                #    print(type(port))
                #for p in ports:
                #    print(p.strip())
                context['boxes'] = Box.objects.filter(boxservice__port__exact=port_int)
                context['search_input'] = search_input
            else:
                context['boxes'] = context['boxes'].filter(Q(ip__icontains=search_input) | Q(hostname__icontains=search_input)) 
                context['search_input'] = search_input
        context['count'] = context['boxes'].count()
        return context

    def post(self, request, *args, **kwargs):
        if 'run_diagram' in request.POST:
            return diagram.create_diagram()
        elif 'run_topology' in request.POST:
            return diagram.create_topology()
        elif 'run_hostlist' in request.POST:
            search_input = self.request.GET.get('search') or ''
            context_boxes = None
            if search_input:
                if 'port=' in search_input:
                    port_string=search_input.split("port=",1)[1]
                    port_int=int(port_string.strip())
                    context_boxes = Box.objects.filter(boxservice__port__exact=port_int)
                else:
                    context_boxes = Box.objects.filter(Q(ip__icontains=search_input) | Q(hostname__icontains=search_input)) 
            else:
                context_boxes = Box.objects.all()
            return diagram.create_hostlist(context_boxes)
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
    fields = ['user', 'hostname', 'os', 'cidr', 'comments', 'active', 'pwned','comeback','unrelated']
    context_object_name='box_form'
    success_url = reverse_lazy('boxes')



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