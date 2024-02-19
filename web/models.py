from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name=models.CharField(max_length=40)

    class Meta:
        ordering=('name',)
        verbose_name_plural='Categories'

    def __str__(self):
        return f"{self.name}"


class Item(models.Model):
    category=models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    description=models.TextField(blank=True, null=True)
    price=models.FloatField()
    image=models.ImageField(upload_to='items_images', blank=True, null=True)
    is_sold=models.BooleanField(default=False)
    created_by=models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at=models.DateTimeField(default=datetime.now, blank=True)
    
    def __str__(self):
        return f"{self.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True )
    balance = models.FloatField(default=10, null=True)

    def __str__(self):
        return f"{self.user.username}"

    def deduct_balance(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False
   

class ProductKey(models.Model):
    key_number = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.key_number

# Create your models here.
