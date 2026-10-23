from django.urls import path
from . import views

app_name = "boutique"

urlpatterns = [
    path("", views.catalogue, name="catalogue"),
    path("produit/<int:pk>/", views.detail_produit, name="detail_produit"),
]
 