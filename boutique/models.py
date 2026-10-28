from django.db import models
 
class Marque(models.Model):
    nom = models.CharField(max_length=80, unique=True)
    description = models.TextField(blank=True)
    pays = models.CharField(max_length=60, blank=True)
 
    class Meta:
        ordering = ["nom"]
 
    def __str__(self):
        return self.nom
 
class Produit(models.Model):
    CATEGORIE_CHOICES = [
        ("vetements", "Vêtements"),
        ("chaussures", "Chaussures"),
        ("accessoires", "Accessoires"),
    ]
    PUBLIC_CHOICES = [
        ("", "Non précisé"),
        ("homme", "Homme"),
        ("femme", "Femme"),
        ("enfant", "Enfant"),
        ("mixte", "Mixte"),
    ]

    nom = models.CharField(max_length=120)
    marque = models.ForeignKey(
        Marque, on_delete=models.PROTECT, related_name="produits")
    categorie = models.CharField(
        max_length=20, choices=CATEGORIE_CHOICES, default="vetements"
    )
    public = models.CharField(
        max_length=10, choices=PUBLIC_CHOICES, blank=True, default=""
    )
    description = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image_fichier = models.CharField(max_length=200, blank=True)
    image_url = models.URLField(blank=True)
    taille = models.CharField(max_length=20, blank=True)
    date_ajout = models.DateField(auto_now_add=True)
 
    class Meta:
        ordering = ["marque__nom", "nom"]
 
    def __str__(self):
        return f"{self.nom} - {self.marque.nom}"


class Commande(models.Model):
    STATUT_CHOICES = [
        ("enregistree", "Enregistrée (démonstration)"),
    ]
    PAIEMENT_CHOICES = [
        ("simulation", "Ancienne simulation générique"),
        ("wave_demo", "Wave — simulation"),
        ("orange_money_demo", "Orange Money — simulation"),
        ("livraison_demo", "Espèces à la livraison — simulation"),
    ]

    nom_client = models.CharField(max_length=120)
    telephone = models.CharField(max_length=30)
    adresse_livraison = models.TextField()
    total = models.DecimalField(max_digits=12, decimal_places=2)
    statut = models.CharField(
        max_length=20, choices=STATUT_CHOICES, default="enregistree"
    )
    mode_paiement = models.CharField(
        max_length=30, choices=PAIEMENT_CHOICES, default="wave_demo"
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_creation"]

    def __str__(self):
        return f"Commande #{self.pk} — {self.nom_client}"


class LigneCommande(models.Model):
    commande = models.ForeignKey(
        Commande, on_delete=models.CASCADE, related_name="lignes"
    )
    produit = models.ForeignKey(
        Produit, on_delete=models.SET_NULL, null=True, blank=True
    )
    nom_produit = models.CharField(max_length=120)
    marque = models.CharField(max_length=80)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    quantite = models.PositiveIntegerField()

    @property
    def sous_total(self):
        return self.prix_unitaire * self.quantite

    def __str__(self):
        return f"{self.nom_produit} × {self.quantite}"