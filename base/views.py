from base.models import Box
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Box

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
    '''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[]
    '''
class BoxDetail(LoginRequiredMixin, DetailView):
    model = Box
    context_object_name = 'box'
    template_name='base/box.html'

class BoxCreate(LoginRequiredMixin, CreateView):
    model = Box
    context_object_name = 'box_form'
    fields = ['user', 'comments', 'active']
    success_url = reverse_lazy('boxes')

class BoxUpdate(LoginRequiredMixin, UpdateView):
    model = Box
    fields = ['user', 'comments', 'active']
    context_object_name='box_form'
    success_url = reverse_lazy('boxes')