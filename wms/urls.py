from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='map/', permanent=True)),
    path('map/', views.index, name='index'),
    path('cells/<int:pk>', views.CellDetailView.as_view(), name='cell-detail'),
    path('places/<int:pk>', views.PlaceDetailView.as_view(), name='place-detail'),
    path('goods/', views.GoodListView.as_view(), name='goods'),
    path('goods/<int:pk>', views.GoodDetailView.as_view(), name='good-detail'),
    path('products/create', views.GoodInstanceCreate.as_view(), name='create-goodinstance'),
    path('products/<int:pk>', views.GoodInstanceDetailView.as_view(), name='goodinstance-detail'),
    path('products/<int:pk>/edit', views.GoodInstanceUpdate.as_view(), name='edit-goodinstance'),
    path('favorites/', views.FavoriteGoodsByUserListView.as_view(), name='favorites'),
    path('favorites/add/<int:pk>', views.add_to_favorites, name='add-to-favorites'),
    path('favorites/remove/<int:pk>', views.remove_from_favorites, name='remove-from-favorites'),
    path('bills/', views.BillListView.as_view(), name='bills'),
    path('bills/<int:pk>', views.BillDetailView.as_view(), name='bill-detail'),
    path('bills/create/', views.BillCreate.as_view(), name='create-bill'),
    path('bills/<int:pk>/edit/', views.BillEdit.as_view(), name='edit-bill'),
    path('bills/<int:bill_id>/add_goodinstance/', views.add_good_to_bill, name='add-good'),
    path('bills/<int:bill_id>/del_goodinstance/<int:goodinstance_id>', views.delete_good_from_bill, name='remove-good'),
    path('cart/', views.cart, name='cart')
]
