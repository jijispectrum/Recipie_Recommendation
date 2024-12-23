from django.urls import path
from .views import login_page, register_page,home,about,contact,recommend_recipes
from.import views
urlpatterns = [
    path('',views.home,name='home'),
    path('login/', login_page, name='login_page'),
    path('register/', register_page, name='register_page'),
    # path('logout/', logout_page, name='logout_page'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('recommend/', views.recommend_recipes, name='recommend_recipes'),
    path('logout/', views.logout_view, name='logout_page'),  # Add this line
    ]



