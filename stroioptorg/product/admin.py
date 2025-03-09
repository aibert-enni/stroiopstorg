from django.contrib import admin

from product.models import Category, Product, Attribute, ProductAttribute, Cart, CartProduct, ProductImage, \
    AttributeValue, FilterAttribute

admin.site.register(Attribute)
admin.site.register(ProductAttribute)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(ProductImage)
admin.site.register(AttributeValue)

class FilterAttributeInline(admin.TabularInline):  # 👈 Можно использовать StackedInline
    model = FilterAttribute
    extra = 1  # Количество пустых строк для добавления новых атрибутов

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # Автозаполнение slug из name

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [FilterAttributeInline]

    list_display = ('name', 'parent')
    list_filter = ('parent',)  # Фильтрация по родительским категориям
    search_fields = ('name',)  # Поиск по имени категории
    ordering = ('parent', 'name',)
    prepopulated_fields = {'slug': ('name',)}  # Автозаполнение slug из name

