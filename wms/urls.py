from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cells/<int:pk>', views.CellDetailView.as_view(), name='cell-detail'),
    path('places/<int:pk>', views.PlaceDetailView.as_view(), name='place-detail'),
    path('goods/<int:pk>', views.GoodDetailView.as_view(), name='good-detail')
]
