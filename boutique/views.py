from django import forms
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Marque, Produit


def accueil(request):
    produits_recents = Produit.objects.select_related("marque").order_by(
        "-pk"
    )[:4]
    produits_disponibles = Produit.objects.select_related("marque").filter(
        stock__gt=0
    ).order_by("-pk")[:4]
    marques = Marque.objects.all()

    return render(request, "boutique/accueil.html", {
        "produits_recents": produits_recents,
        "produits_disponibles": produits_disponibles,
        "marques": marques,
    })


def catalogue(request):
    produits = Produit.objects.select_related("marque").all()
    marques = Marque.objects.all()

    recherche = request.GET.get("q", "").strip()
    marque_id = request.GET.get("marque", "")
    categorie = request.GET.get("categorie", "")
    taille = request.GET.get("taille", "").strip()
    prix_min = request.GET.get("prix_min", "").strip()
    prix_max = request.GET.get("prix_max", "").strip()
    tri = request.GET.get("tri", "")
    disponible = request.GET.get("disponible", "") == "1"

    if recherche:
        produits = produits.filter(
            nom__icontains=recherche
        ) | produits.filter(marque__nom__icontains=recherche)

    if marque_id.isdigit():
        produits = produits.filter(marque_id=int(marque_id))

    categorie_values = {value for value, _ in Produit.CATEGORIE_CHOICES}
    if categorie in categorie_values:
        produits = produits.filter(categorie=categorie)

    if taille:
        size_filter = Q(taille__iexact=taille) | Q(taille__icontains=taille)
        if taille.isdecimal():
            requested_size = int(taille)
            ranged_sizes = []
            for product_id, available_size in produits.exclude(
                taille=""
            ).values_list("pk", "taille"):
                bounds = available_size.split("-", maxsplit=1)
                if len(bounds) != 2:
                    continue
                try:
                    lower_bound, upper_bound = map(int, bounds)
                except ValueError:
                    continue
                if lower_bound <= requested_size <= upper_bound:
                    ranged_sizes.append(product_id)
            size_filter |= Q(pk__in=ranged_sizes)
        produits = produits.filter(size_filter)

    if prix_min:
        try:
            minimum = forms.DecimalField(min_value=0).clean(prix_min)
        except forms.ValidationError:
            minimum = None
        if minimum is not None:
            produits = produits.filter(prix__gte=minimum)

    if prix_max:
        try:
            maximum = forms.DecimalField(min_value=0).clean(prix_max)
        except forms.ValidationError:
            maximum = None
        if maximum is not None:
            produits = produits.filter(prix__lte=maximum)

    if disponible:
        produits = produits.filter(stock__gt=0)

    if tri == "prix-croissant":
        produits = produits.order_by("prix", "nom")
    elif tri == "prix-decroissant":
        produits = produits.order_by("-prix", "nom")
    elif tri == "nouveautes":
        produits = produits.order_by("-pk")

    return render(request, "boutique/catalogue.html", {
        "produits": produits,
        "marques": marques,
        "categories": Produit.CATEGORIE_CHOICES,
        "recherche": recherche,
        "marque_selectionnee": marque_id,
        "categorie_selectionnee": categorie,
        "taille_selectionnee": taille,
        "prix_min": prix_min,
        "prix_max": prix_max,
        "tri_selectionne": tri,
        "disponible_selectionne": disponible,
    })


def detail_produit(request, pk):
    produit = get_object_or_404(
        Produit.objects.select_related("marque"), pk=pk
    )

    return render(request, "boutique/detail_produit.html", {
        "produit": produit,
    })
