from django.test import TestCase

from .models import Marque, Produit


class BoutiquePagesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.nike = Marque.objects.create(nom="Test Nike")
        cls.zara = Marque.objects.create(nom="Test Zara")
        Produit.objects.create(
            nom="Baskets sport",
            marque=cls.nike,
            categorie="chaussures",
            description="Chaussures de sport",
            prix="45000.00",
            stock=4,
            taille="42",
            image_fichier="boutique/images/baskets-sport.jpg",
        )
        Produit.objects.create(
            nom="Veste beige",
            marque=cls.zara,
            categorie="vetements",
            prix="65000.00",
            stock=0,
            taille="M",
        )
        Produit.objects.create(
            nom="Sac urbain",
            marque=cls.zara,
            categorie="accessoires",
            prix="25000.00",
            stock=2,
            taille="Unique",
        )

    def test_homepage_renders_brand_and_catalogue_link(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "URBAN")
        self.assertContains(response, "Les nouveautés")
        self.assertContains(response, "Découvrir la collection")

    def test_catalogue_filters_by_category(self):
        response = self.client.get(
            "/catalogue/",
            {"categorie": "chaussures"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Baskets sport")
        self.assertNotContains(response, "Veste beige")

    def test_catalogue_combines_price_size_and_availability_filters(self):
        response = self.client.get(
            "/catalogue/",
            {
                "prix_min": "30000",
                "prix_max": "50000",
                "taille": "42",
                "disponible": "1",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Baskets sport")
        self.assertNotContains(response, "Veste beige")
        self.assertNotContains(response, "Sac urbain")

    def test_numeric_size_matches_available_size_ranges(self):
        response = self.client.get(
            "/catalogue/",
            {"taille": "42", "categorie": "chaussures"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Chaussures de running légères")

    def test_catalogue_sorts_prices_ascending(self):
        response = self.client.get(
            "/catalogue/",
            {"tri": "prix-croissant"},
        )

        self.assertEqual(response.status_code, 200)
        products = list(response.context["produits"])
        self.assertEqual(
            [product.prix for product in products],
            sorted(product.prix for product in products),
        )

    def test_invalid_price_filter_does_not_break_catalogue(self):
        baseline = self.client.get("/catalogue/")
        response = self.client.get("/catalogue/", {"prix_min": "not-a-price"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["produits"].values_list("pk", flat=True)),
            list(baseline.context["produits"].values_list("pk", flat=True)),
        )

    def test_product_detail_uses_urbanwear_branding(self):
        product = Produit.objects.get(nom="Baskets sport")
        response = self.client.get(f"/produit/{product.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "UrbanWear")
        self.assertContains(response, "45000")

    def test_store_products_have_categories(self):
        self.assertFalse(Produit.objects.filter(categorie="").exists())
        self.assertSetEqual(
            set(Produit.objects.values_list("categorie", flat=True).distinct()),
            {"vetements", "chaussures", "accessoires"},
        )
