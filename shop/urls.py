from django.urls import path
from . import views

urlpatterns = [
   path('',views.home,name="home"),
   path('home',views.home,name="home"),
   path('register',views.register,name="register"),
   path('login',views.loginpage,name="login"),
   path('logout',views.logoutview,name="logout"),
   path('Feedback',views.Feedback,name="feedback"),
   path('collections',views.collections,name="collections"),
    path('collections/<str:name>',views.collectionsview,name="collections"),
    path('collections/<str:cname>/<str:pname>',views.productdetails,name="productdetails")
]
