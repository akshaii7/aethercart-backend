from django.db import models

class Product(models.Model):
     
     CATEGORY_CHOICES =(
          ('electronics','Electronics'),
          ('grocery','Grocery'),
          ('fashion','Fashion'),
          ('beauty','Beauty'),
          ('home','Home'),
          
          
     )
     
     name = models.CharField(max_length=100)
     brand = models.CharField(
          max_length=100,
          blank=True,
          null = True
          
     )
     
     description = models.TextField(blank=True)
     price = models.DecimalField(max_digits=10,decimal_places=2)
     stock = models.PositiveBigIntegerField(default=0)
     
     
     category = models.CharField(
          max_length=50,
          choices=CATEGORY_CHOICES,
          default='grocery'
     )
     
     image = models.ImageField(
          upload_to ='products/',
          blank=True,
          null=True
     )
     
     
     
     is_available = models.BooleanField(default=True)
     
     created_at = models.DateTimeField(auto_now_add=True)
     
     def __str__(self):
          return self.name