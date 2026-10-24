from django.db import migrations, models


def classify_products(apps, schema_editor):
    Produit = apps.get_model("boutique", "Produit")
    database = schema_editor.connection.alias

    for product_id, name in Produit.objects.using(database).values_list(
        "pk", "nom"
    ):
        name = name.lower()
        if any(term in name for term in ("sac", "casquette", "accessoire")):
            category = "accessoires"
        elif any(
            term in name
            for term in ("basket", "sneaker", "chaussure", "botte")
        ):
            category = "chaussures"
        else:
            category = "vetements"
        Produit.objects.using(database).filter(pk=product_id).update(
            categorie=category
        )


class Migration(migrations.Migration):
    dependencies = [
        ("boutique", "0003_add_more_products_and_unique_photos"),
    ]

    operations = [
        migrations.AddField(
            model_name="produit",
            name="categorie",
            field=models.CharField(
                choices=[
                    ("vetements", "Vêtements"),
                    ("chaussures", "Chaussures"),
                    ("accessoires", "Accessoires"),
                ],
                default="vetements",
                max_length=20,
            ),
        ),
        migrations.RunPython(classify_products, migrations.RunPython.noop),
    ]
