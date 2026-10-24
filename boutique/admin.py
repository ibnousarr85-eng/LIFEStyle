# Register your models here.
from django.contrib import admin
from .models import Marque, Produit

@admin.register(Marque)
class MarqueAdmin(admin.ModelAdmin):
	list_display = ("nom", "pays")
	search_fields = ("nom", "pays")

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
	list_display = ("nom", "marque", "categorie", "prix", "stock", "taille")
	list_filter = ("marque", "categorie")
	search_fields = ("nom", "marque__nom")
