from django.db import migrations


AUDIENCE_ASSIGNMENTS = {
    "homme": [
        "T-shirt Nike Sportswear",
        "Veste bomber Adidas Essentials",
        "Baskets Puma RS-X",
        "Pantalon Nike Club Fleece",
        "T-shirt Adidas Originals",
        "Sweat Puma Essentials",
        "Jean droit 501",
        "Baskets streetwear rouge et noir",
        "Baskets de running grises",
        "Chemise blanche classique",
        "Sneakers en toile montantes",
        "Sweatshirt noir classique",
        "Chaussures de running légères",
        "Baskets rétro multicolores",
        "Bottes en cuir marron",
        "T-shirt noir imprimé",
    ],
    "femme": [
        "Veste en cuir",
        "Robe rouge élégante",
        "Sac à main rouge",
        "Manteau long camel",
        "Top violet épaules dénudées",
        "Sac bandoulière noir",
    ],
    "mixte": [
        "Sac à dos urbain",
        "Casquette sport blanche",
        "Sac à dos bordeaux",
    ],
}

CHILD_PRODUCTS = [
    {
        "nom": "Cardigan bleu enfant",
        "description": "Un cardigan confortable pour composer une tenue soignée au quotidien.",
        "categorie": "vetements",
        "public": "enfant",
        "prix": "18900.00",
        "stock": 8,
        "taille": "4-10 ans",
        "image_url": (
            "https://images.unsplash.com/"
            "photo-1519238263530-99bdd11df2ea?w=800&q=85"
        ),
    },
    {
        "nom": "Tenue décontractée enfant",
        "description": "Une tenue légère et confortable pour bouger et jouer.",
        "categorie": "vetements",
        "public": "enfant",
        "prix": "22500.00",
        "stock": 6,
        "taille": "4-10 ans",
        "image_url": (
            "https://images.unsplash.com/"
            "photo-1519457431-44ccd64a579b?w=800&q=85"
        ),
    },
]


def populate_audience_collections(apps, schema_editor):
    Marque = apps.get_model("boutique", "Marque")
    Produit = apps.get_model("boutique", "Produit")
    database = schema_editor.connection.alias

    for audience, product_names in AUDIENCE_ASSIGNMENTS.items():
        Produit.objects.using(database).filter(
            public="",
            nom__in=product_names,
        ).update(public=audience)

    brand, _ = Marque.objects.using(database).get_or_create(
        nom="UrbanWear Kids",
        defaults={
            "description": "Une sélection confortable et colorée pour les enfants.",
            "pays": "Sélection UrbanWear",
        },
    )
    for product_data in CHILD_PRODUCTS:
        Produit.objects.using(database).get_or_create(
            marque=brand,
            nom=product_data["nom"],
            defaults=product_data,
        )


def reverse_audience_collections(apps, schema_editor):
    Marque = apps.get_model("boutique", "Marque")
    Produit = apps.get_model("boutique", "Produit")
    database = schema_editor.connection.alias

    for audience, product_names in AUDIENCE_ASSIGNMENTS.items():
        Produit.objects.using(database).filter(
            public=audience,
            nom__in=product_names,
        ).update(public="")

    child_brand = Marque.objects.using(database).filter(
        nom="UrbanWear Kids"
    ).first()
    if child_brand is None:
        return

    for product_data in CHILD_PRODUCTS:
        Produit.objects.using(database).filter(
            marque=child_brand,
            nom=product_data["nom"],
            image_url=product_data["image_url"],
        ).delete()
    if not child_brand.produits.exists():
        child_brand.delete()


class Migration(migrations.Migration):
    dependencies = [
        ("boutique", "0006_produit_image_url_produit_public"),
    ]

    operations = [
        migrations.RunPython(
            populate_audience_collections,
            reverse_audience_collections,
        ),
    ]
