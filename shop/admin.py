from django.contrib import admin
from .models import Item, Cart, CartItem, Order

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'rarity', 'price', 'stock')
    list_filter = ('category', 'rarity')
    search_fields = ('name',)

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)