from django.urls import path

from img_resizer import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('<str:image_hash>/', views.image_view, name='image_view')
]
