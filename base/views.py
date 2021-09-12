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
from .models import Box, BoxService
from .forms import UploadFileForm 
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import classonlymethod, method_decorator
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.conf import settings
from webpush import send_user_notification

#pip install --upgrade pip
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
            #context['boxes'] = context['boxes'].filter(boxservice__port=search_input) 
            context['boxes'] = context['boxes'].filter(Q(ip__icontains=search_input) | Q(hostname__icontains=search_input)) 
        context['search_input'] = search_input
        context['count'] = context['boxes'].count()
        context['services_count'] = BoxService.objects.count()
        return context

    def get(self, request, *args, **kwargs):
        webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
        vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
        user = request.user


        return render(request, 'base/box_list.html', {user: user, 'vapid_key': vapid_key})
    #def post(self, *args, **kwargs):
    #    if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            #new_box = Box.objects.filter(browserupdate=True)
            #new_service = BoxService.objects.filter(browserupdate=True)
            #new_service = BoxService.objects.filter(Q(new=True) | Q(updated=True))
            #if new_box or new_service:
                #BoxService.objects.all().update(new=False, updated=False)
    #        return HttpResponse(status=200)
            #else:
            #    return HttpResponse(status=400)
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
    fields = ['user', 'hostname', 'os', 'comments', 'active', 'pwned']
    context_object_name='box_form'
    success_url = reverse_lazy('boxes')


@require_POST
@csrf_exempt
def send_push(request):
    try:
        body = request.body
        data = json.loads(body)

        if 'head' not in data or 'body' not in data or 'id' not in data:
            return JsonResponse(status=400, data={"message": "Invalid data format"})

        user_id = data['id']
        user = get_object_or_404(User, pk=user_id)
        payload = {'head': data['head'], 'body': data['body']}
        send_user_notification(user=user, payload=payload, ttl=1000)

        return JsonResponse(status=200, data={"message": "Web push successful"})
    except TypeError:
        return JsonResponse(status=500, data={"message": "An error occurred"})


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