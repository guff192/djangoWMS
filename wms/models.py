from django.db import models


class GoodTypes(models.Model):
    barcode = models.IntegerField
    article = models.CharField
    weight = models.IntegerField
    price = models.IntegerField
    fragile = models.BooleanField


class Cell(models.Model):
    row = models.CharField
    place = models.CharField


class StoragePlaces(models.Model):
    cell_id = models.ForeignKey(Cell, on_delete=models.CASCADE)
    type = models.CharField
    length = models.IntegerField
    width = models.IntegerField
    height = models.IntegerField
    max_weight = models.IntegerField


class Bills(models.Model):
    number = models.IntegerField
    operation_type = models.IntegerField
    date = models.DateField


class Goods(models.Model):
    barcode = models.ForeignKey(GoodTypes, on_delete=models.CASCADE)
    manufactured = models.DateField
    best_before = models.DateField
    BillsGoods = models.ManyToManyField(Bills)
    PlacesGoods = models.ManyToManyField(StoragePlaces)

