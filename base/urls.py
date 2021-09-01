from django.urls import path
from . import views
from .views import BoxUpdate, Boxes, BoxDetail, BoxCreate, BoxUpdate, CustomLoginView, RegisterPage, BoxUpload
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', Boxes.as_view(), name="boxes"),
    path('box/<int:pk>', BoxDetail.as_view(), name="box-detail"),
    path('create-box/', BoxCreate.as_view(), name="box-create"),
    path('update-box/<int:pk>', BoxUpdate.as_view(), name="box-update"),
    path('upload/', BoxUpload.as_view(), name="box-upload")
]

urlpatterns += static(settings.NMAP_URL, document_root=settings.NMAP_ROOT)