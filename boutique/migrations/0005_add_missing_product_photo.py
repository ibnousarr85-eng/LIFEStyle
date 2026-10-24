from django.db import migrations


def add_missing_product_photo(apps, schema_editor):
    Produit = apps.get_model("boutique", "Produit")
    Produit.objects.using(schema_editor.connection.alias).filter(
        nom="Baskets Puma RS-X",
        image_fichier="",
    ).update(image_fichier="boutique/images/baskets-sport.jpg")


class Migration(migrations.Migration):
    dependencies = [
        ("boutique", "0004_add_product_categories"),
    ]

    operations = [
        migrations.RunPython(
            add_missing_product_photo,
            migrations.RunPython.noop,
        ),
    ]
