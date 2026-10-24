from django.db import migrations


def add_catalogue_products(apps, schema_editor):
    Marque = apps.get_model("boutique", "Marque")
    Produit = apps.get_model("boutique", "Produit")
    database = schema_editor.connection.alias

    brands = [
        {
            "nom": "Nike",
            "description": "Vêtements et chaussures de sport.",
            "pays": "États-Unis",
        },
        {
            "nom": "Levi's",
            "description": "Jeans et essentiels en denim.",
            "pays": "États-Unis",
        },
        {
            "nom": "Zara",
            "description": "Mode contemporaine et pièces tendance.",
            "pays": "Espagne",
        },
        {
            "nom": "H&M",
            "description": "Vêtements et essentiels du quotidien.",
            "pays": "Suède",
        },
        {
            "nom": "Salvatore Ferragamo",
            "description": "Maroquinerie et accessoires de luxe.",
            "pays": "Italie",
        },
    ]

    brand_records = {}
    for brand_data in brands:
        brand, _ = Marque.objects.using(database).get_or_create(
            nom=brand_data["nom"],
            defaults={
                "description": brand_data["description"],
                "pays": brand_data["pays"],
            },
        )
        brand_records[brand_data["nom"]] = brand

    products = [
        {
            "marque": "Levi's",
            "nom": "Jean droit 501",
            "description": "Jean droit en denim, une pièce essentielle du vestiaire.",
            "prix": "39900.00",
            "stock": 12,
            "image_fichier": "boutique/images/jean-levis.jpg",
            "taille": "28-36",
        },
        {
            "marque": "Zara",
            "nom": "Veste en cuir",
            "description": "Veste noire au style urbain, idéale pour la mi-saison.",
            "prix": "69000.00",
            "stock": 7,
            "image_fichier": "boutique/images/veste-zara.jpg",
            "taille": "S-XL",
        },
        {
            "marque": "Zara",
            "nom": "Robe rouge élégante",
            "description": "Robe rouge fluide pour les occasions et les sorties.",
            "prix": "54900.00",
            "stock": 5,
            "image_fichier": "boutique/images/robe-zara.jpg",
            "taille": "S-XL",
        },
        {
            "marque": "H&M",
            "nom": "Chemise blanche classique",
            "description": "Chemise blanche à manches longues pour une tenue soignée.",
            "prix": "24900.00",
            "stock": 14,
            "image_fichier": "boutique/images/chemise-homme.jpg",
            "taille": "S-XXL",
        },
        {
            "marque": "Salvatore Ferragamo",
            "nom": "Sac à main rouge",
            "description": "Sac à main structuré avec poignée et fermoir métallique.",
            "prix": "225000.00",
            "stock": 3,
            "image_fichier": "boutique/images/sac-ferragamo.jpg",
            "taille": "Unique",
        },
        {
            "marque": "Nike",
            "nom": "Baskets streetwear rouge et noir",
            "description": "Baskets montantes au style streetwear.",
            "prix": "74900.00",
            "stock": 8,
            "image_fichier": "boutique/images/nike-baskets-rouge.jpg",
            "taille": "39-44",
        },
        {
            "marque": "Nike",
            "nom": "Baskets de running grises",
            "description": "Chaussures de sport légères pour la course et le quotidien.",
            "prix": "85900.00",
            "stock": 10,
            "image_fichier": "boutique/images/nike-running.jpg",
            "taille": "39-44",
        },
    ]

    for product_data in products:
        brand_name = product_data.pop("marque")
        Produit.objects.using(database).get_or_create(
            marque=brand_records[brand_name],
            nom=product_data["nom"],
            defaults=product_data,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("boutique", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_catalogue_products, migrations.RunPython.noop),
    ]
