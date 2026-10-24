from django.db import migrations


def expand_catalogue(apps, schema_editor):
    Marque = apps.get_model("boutique", "Marque")
    Produit = apps.get_model("boutique", "Produit")
    database = schema_editor.connection.alias

    brands = [
        {
            "nom": "Converse",
            "description": "Sneakers en toile et vêtements au style urbain.",
            "pays": "États-Unis",
        },
        {
            "nom": "New Balance",
            "description": "Chaussures et vêtements de sport.",
            "pays": "États-Unis",
        },
        {
            "nom": "Mango",
            "description": "Vêtements et accessoires contemporains.",
            "pays": "Espagne",
        },
        {
            "nom": "Timberland",
            "description": "Chaussures et vêtements inspirés du plein air.",
            "pays": "États-Unis",
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

    updates = [
        (
            "Adidas",
            "Sweat Adidas Essentials",
            "Veste bomber Adidas Essentials",
            "boutique/images/newbalance-jacket.jpg",
        ),
        (
            "Puma",
            "Sweat Puma Essentials",
            "Sweat Puma Essentials",
            "boutique/images/hoodie-puma.jpg",
        ),
    ]
    for brand_name, old_name, new_name, image_path in updates:
        Produit.objects.using(database).filter(
            marque__nom=brand_name,
            nom=old_name,
        ).filter(image_fichier="").update(
            nom=new_name,
            image_fichier=image_path,
        )
        if old_name != new_name:
            Produit.objects.using(database).filter(
                marque__nom=brand_name,
                nom=old_name,
                image_fichier="boutique/images/veste-denim-dakar.jpg",
            ).update(nom=new_name, image_fichier=image_path)

    Produit.objects.using(database).filter(
        marque__nom="Puma",
        nom="Sweat Puma Essentials",
        image_fichier="boutique/images/robe-niani.jpg",
    ).update(image_fichier="boutique/images/sweat-puma.jpg")

    products = [
        {
            "marque": "Converse",
            "nom": "Sneakers en toile montantes",
            "description": "Chaussures en toile au style urbain et décontracté.",
            "prix": "45900.00",
            "stock": 9,
            "image_fichier": "boutique/images/alt-sneakers.jpg",
            "taille": "36-44",
        },
        {
            "marque": "Converse",
            "nom": "Sac à dos urbain",
            "description": "Sac à dos compact avec compartiment principal zippé.",
            "prix": "32900.00",
            "stock": 11,
            "image_fichier": "boutique/images/converse-backpack.jpg",
            "taille": "Unique",
        },
        {
            "marque": "Converse",
            "nom": "Sweatshirt noir classique",
            "description": "Sweatshirt confortable à porter au quotidien.",
            "prix": "39900.00",
            "stock": 8,
            "image_fichier": "boutique/images/alt-hoodie.jpg",
            "taille": "S-XL",
        },
        {
            "marque": "New Balance",
            "nom": "Chaussures de running légères",
            "description": "Chaussures légères pour les sorties de course et le quotidien.",
            "prix": "79900.00",
            "stock": 7,
            "image_fichier": "boutique/images/newbalance-running.jpg",
            "taille": "39-45",
        },
        {
            "marque": "New Balance",
            "nom": "Casquette sport blanche",
            "description": "Casquette légère à visière courbée.",
            "prix": "18900.00",
            "stock": 15,
            "image_fichier": "boutique/images/newbalance-cap.jpg",
            "taille": "Unique",
        },
        {
            "marque": "New Balance",
            "nom": "Baskets rétro multicolores",
            "description": "Baskets basses au look rétro et à la semelle confortable.",
            "prix": "69900.00",
            "stock": 6,
            "image_fichier": "boutique/images/converse-canvas.jpg",
            "taille": "39-45",
        },
        {
            "marque": "Mango",
            "nom": "Manteau long camel",
            "description": "Manteau ceinturé pour la mi-saison.",
            "prix": "89900.00",
            "stock": 4,
            "image_fichier": "boutique/images/mango-trench.jpg",
            "taille": "S-XL",
        },
        {
            "marque": "Mango",
            "nom": "Top violet épaules dénudées",
            "description": "Top élégant à encolure bardot.",
            "prix": "29900.00",
            "stock": 10,
            "image_fichier": "boutique/images/alt-dress.jpg",
            "taille": "S-L",
        },
        {
            "marque": "Mango",
            "nom": "Sac bandoulière noir",
            "description": "Sac noir à bandoulière pour les sorties et le quotidien.",
            "prix": "42900.00",
            "stock": 5,
            "image_fichier": "boutique/images/mango-bag.jpg",
            "taille": "Unique",
        },
        {
            "marque": "Timberland",
            "nom": "Bottes en cuir marron",
            "description": "Bottes montantes à lacets avec semelle robuste.",
            "prix": "109900.00",
            "stock": 6,
            "image_fichier": "boutique/images/timberland-boots.jpg",
            "taille": "40-45",
        },
        {
            "marque": "Timberland",
            "nom": "T-shirt noir imprimé",
            "description": "T-shirt à manches courtes pour une tenue décontractée.",
            "prix": "24900.00",
            "stock": 12,
            "image_fichier": "boutique/images/alt-shirt.jpg",
            "taille": "S-XXL",
        },
        {
            "marque": "Timberland",
            "nom": "Sac à dos bordeaux",
            "description": "Sac à dos en matière souple avec poche extérieure.",
            "prix": "49900.00",
            "stock": 5,
            "image_fichier": "boutique/images/alt-backpack.jpg",
            "taille": "Unique",
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
        ("boutique", "0002_expand_catalogue"),
    ]

    operations = [
        migrations.RunPython(expand_catalogue, migrations.RunPython.noop),
    ]
