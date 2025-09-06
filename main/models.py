import uuid
from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('apparel', 'Apparel'),       # jersey & clothing
        ('footwear', 'Footwear'),     # sepatu bola / futsal
        ('equipment', 'Equipment'),   # bola, gawang, alat latihan
        ('accessories', 'Accessories'), # shin guard, gloves, tas
        ('merch', 'Merchandise'),     # souvenir, topi, scarf
    ]

    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)  
    price = models.IntegerField()  
    description = models.TextField()  
    thumbnail = models.URLField(blank=True, null=True)  
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)  
    is_featured = models.BooleanField(default=False)  
    rating = models.FloatField(default=0.0)
    stock = models.PositiveIntegerField(default=0)
    brand = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
    
    @property
    def is_highly_rated(self):
        return self.rating > 20
        
    # def increment_views(self):
    #     self.news_views += 1
    #     self.save()