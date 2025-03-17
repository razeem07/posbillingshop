from django.db import models

# category,product,order,orderItems

class Category(models.Model):

    name=models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):

    title=models.CharField(max_length=120,unique=True)

    description=models.TextField()

    price=models.DecimalField(max_digits=5,decimal_places=2)

    category_object=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products")

    def __str__(self):
        return self.title
    
class Order(models.Model):

    phone=models.CharField(max_length=15)

    created_at=models.DateTimeField(auto_now_add=True)

    status=models.BooleanField(default=False)

    total=models.DecimalField(max_digits=8,decimal_places=2,null=True)


class OrderItems(models.Model):


    order_object=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items")

    product_object=models.ForeignKey(Product,on_delete=models.CASCADE)

    qty=models.DecimalField(max_digits=6,decimal_places=3,default=0.0)














