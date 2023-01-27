from django.urls import path
from main.views import *


urlpatterns = [
    path('', AvtobusHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('category/<slug:post_slug>/', show_post, name='post'),
    path('category/', show_category, name='category'),
    path('download/', download, name='download'),
    path('save/<str:date>/<str:date_end>', save, name='save'),



]