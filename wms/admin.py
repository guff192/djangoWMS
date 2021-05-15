from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(GoodInstance)
class GoodInstanceAdmin(admin.ModelAdmin):
    list_display = ('good', 'place')
    list_filter = ('good', ('place__cell', admin.RelatedOnlyFieldListFilter), 'place__level', 'bill')


class GoodInstanceInline(admin.TabularInline):
    model = GoodInstance
    extra = 0


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    list_filter = ('manufacturer', 'model', 'fragile')
    inlines = [
        GoodInstanceInline,
    ]


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('number', 'date', 'operation')
    list_filter = ('operation',)
    inlines = [
        GoodInstanceInline,
    ]


class CellInline(admin.TabularInline):
    model = Cell
    extra = 0


@admin.register(Row)
class RowAdmin(admin.ModelAdmin):
    list_filter = ('storage',)
    inlines = [
        CellInline,
    ]


class PlaceInline(admin.TabularInline):
    model = Place
    extra = 0


@admin.register(Cell)
class CellAdmin(admin.ModelAdmin):
    list_filter = ('row', 'section')
    inlines = [
        PlaceInline,
    ]


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('level', 'row', 'section')
    list_filter = ('cell__row', 'cell__section', 'cell__row__storage')
    inlines = [
        GoodInstanceInline,
    ]

    @admin.display(description='(Storage type) Row number')
    def row(self, obj):
        return str(obj.cell.row)

    @admin.display(description='Section number')
    def section(self, obj):
        return str(obj.cell.section)
