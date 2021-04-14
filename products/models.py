from django.db import models

# Create your models here.

class Menu(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = "menu"


class MainCategory(models.Model):
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE)
    name = models.CharField(max_length=45)

    class Meta:
        db_table = "main_categories"


class SubCategory(models.Model):
    main_category = models.ForeignKey('MainCategory', on_delete=models.CASCADE)
    name = models.CharField(max_length=45)

    class Meta:
        db_table = "sub_categories"


class Product(models.Model):
    name          = models.CharField(max_length=45)
    price         = models.IntegerField()
    hashtag       = models.CharField(max_length=45)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)
    main_category = models.ForeignKey('MainCategory', on_delete=models.CASCADE)
    sub_category  = models.ForeignKey('SubCategory', on_delete=models.CASCADE)

    class Meta:
        db_table = "products"


class ProductImage(models.Model):
    image_url = models.CharField(max_length=2000)
    product   = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = "product_images"


class ProductOption(models.Model):
    weight     = models.IntegerField()
    extra_cost = models.IntegerField()
    product    = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = "product_options"


class Labels(models.Model):
    name    = models.CharField(max_length=45)
    color   = models.CharField(max_length=45)
    product = models.ManyToManyField('Product', through='ProductsLabels')

    class Meta:
        db_table = "labels"


class ProductsLabels(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    labels  = models.ForeignKey(Labels, on_delete=models.CASCADE)

    class Meta:
        db_table = "products_labels"

