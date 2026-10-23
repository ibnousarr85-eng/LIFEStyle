from django.shortcuts import get_object_or_404, render

from .models import Marque, Produit


def catalogue(request):
    produits = Produit.objects.select_related("marque").all()
    marques = Marque.objects.all()

    recherche = request.GET.get("q", "").strip()
    marque_id = request.GET.get("marque", "")

    if recherche:
        produits = produits.filter(nom__icontains=recherche)

    if marque_id.isdigit():
        produits = produits.filter(marque_id=int(marque_id))

    return render(request, "boutique/catalogue.html", {
        "produits": produits,
        "marques": marques,
        "recherche": recherche,
        "marque_selectionnee": marque_id,
    })


def detail_produit(request, pk):
    produit = get_object_or_404(
        Produit.objects.select_related("marque"), pk=pk
    )

    return render(request, "boutique/detail_produit.html", {
        "produit": produit,
    })
