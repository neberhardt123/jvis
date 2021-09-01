from django.urls import path
from . import views
from .views import BoxUpdate, Boxes, BoxDetail, BoxCreate, BoxUpdate, CustomLoginView, RegisterPage
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', Boxes.as_view(), name="boxes"),
    path('box/<int:pk>', BoxDetail.as_view(), name="box-detail"),
    path('create-box/', BoxCreate.as_view(), name="box-create"),
    path('update-box/<int:pk>', BoxUpdate.as_view(), name="box-update"),
]