from django.urls import path

from . import views

urlpatterns = [
    #path('', views.IndexView.as_view(), name='Index'),
    path('', views.TextView.as_view(), name='Test'),

    path('categories/', views.CategoriesView.as_view(), name='Categories'),

    path('category/', views.CategoryView.as_view(), name='Category'),
    path('category/<uuid:category_uuid>', views.CategoryView.as_view(), name='Category1'),
    path('category/<str:category_title>', views.CategoryView.as_view(), name='Category2'),

    path('thinghistory/<uuid:thing>', views.CategoryView.as_view(), name='History'),
    path('about/', views.AboutView.as_view()),
]
