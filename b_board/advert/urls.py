""" URL configuration for advert app """
from django.urls import path
from .views import *


urlpatterns = [
    path('', MainPage.as_view(), name='main'),     
    path('category/<int:category_id>', MainPage.as_view(), name='adverts_from_category'),
    path('get-adverts/', get_adverts, name='get_adverts'),
    path('advert/<int:pk>', OneAdvert.as_view(), name = 'one_advert'),
    path('create/', CreateAdver.as_view(), name = 'create_adver'),
    path('update/<int:pk>', UpdateAdvert.as_view(), name = 'update_advert'),
    path('delete/<int:pk>', DeleteAdvert.as_view(), name = 'delete_advert'),
    path('comment-add/', comment_add, name = 'comment_add'),
    path('comment-accept/', comment_accept, name = 'comment_accept'),
    path('comment-delete/', comment_delete, name = 'comment_delete'),
    path('comment-get-update-form/', comment_get_update_form, name = 'comment_get_update_form'),
    path('comment-get-add-form/', comment_get_add_form, name = 'comment_get_add_form'),
    path('comment-update/<int:pk>', comment_update, name = 'comment_update'),
    path('user-page/', UserPage.as_view(), name = 'user_page'),
]
