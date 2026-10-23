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
    nom = models.CharField(max_length=120)
    marque = models.ForeignKey(
        Marque, on_delete=models.PROTECT, related_name="produits")
    description = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image_fichier = models.CharField(max_length=200, blank=True)
    taille = models.CharField(max_length=20, blank=True)
    date_ajout = models.DateField(auto_now_add=True)
 
    class Meta:
        ordering = ["marque__nom", "nom"]
 
    def __str__(self):
        return f"{self.nom} - {self.marque.nom}"