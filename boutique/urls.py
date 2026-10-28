from django.urls import path
from . import views

app_name = "boutique"

urlpatterns = [
    path("", views.accueil, name="accueil"),
    path("catalogue/", views.catalogue, name="catalogue"),
    path("marques/", views.nos_marques, name="nos_marques"),
    path("produit/<int:pk>/", views.detail_produit, name="detail_produit"),
]
 