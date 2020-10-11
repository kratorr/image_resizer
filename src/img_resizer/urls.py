from django.urls import path

from img_resizer import views


urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('<str:image_hash>/', views.image_view, name='image_view')
] 