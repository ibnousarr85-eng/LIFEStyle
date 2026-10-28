# Register your models here.
from django.contrib import admin
from .models import Commande, LigneCommande, Marque, Produit

@admin.register(Marque)
class MarqueAdmin(admin.ModelAdmin):
	list_display = ("nom", "pays")
	search_fields = ("nom", "pays")

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
	list_display = ("nom", "marque", "categorie", "public", "prix", "stock", "taille")
	list_filter = ("marque", "categorie", "public")
	search_fields = ("nom", "marque__nom")


class LigneCommandeInline(admin.TabularInline):
	model = LigneCommande
	extra = 0
	readonly_fields = ("produit", "nom_produit", "marque", "prix_unitaire", "quantite")


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
	list_display = ("id", "nom_client", "telephone", "total", "statut", "date_creation")
	list_filter = ("statut", "date_creation")
	search_fields = ("nom_client", "telephone")
	readonly_fields = (
		"nom_client",
		"telephone",
		"adresse_livraison",
		"total",
		"statut",
		"date_creation",
	)
	inlines = (LigneCommandeInline,)
