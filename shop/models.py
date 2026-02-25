from django.db import models, transaction
from django.conf import settings

class Item(models.Model):
    # Categorize the loot
    CATEGORY_CHOICES = [
        ('WEAPON', 'Weapon'),
        ('ARMOR', 'Armor'),
        ('POTION', 'Potion'),
        ('REAGENT', 'Crafting Material'),
        ('FOOD', 'Food & Drink'),
    ]

    RARITY_CHOICES = [
        ('COMMON', 'Common (Grey)'),
        ('RARE', 'Rare (Blue)'),
        ('EPIC', 'Epic (Purple)'),
        ('LEGENDARY', 'Legendary (Gold)'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='WEAPON')
    rarity = models.CharField(max_length=10, choices=RARITY_CHOICES, default='COMMON')
    
    # Economics
    price = models.PositiveIntegerField(help_text="Price in Gold Pieces")
    stock = models.PositiveIntegerField(default=1)
    
    # Visuals (Optional for now, but ready for design later)
    image_url = models.URLField(blank=True, null=True, help_text="Link to an icon or sprite")

    def __str__(self):
        return f"{self.name} ({self.rarity})"
    
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    def get_total_gold(self):
        # Logic to sum up all items in this cart
        return sum(item.item.price * item.quantity for item in self.items.all())
    
    def process_checkout(self):
        profile = self.user.profile
        total_cost = self.get_total_gold()

        # Wrap in a transaction so if one thing fails, nothing changes
        with transaction.atomic():
            if profile.gold < total_cost:
                return False, "Not enough gold!"

            summary_list = []
            for cart_item in self.items.all():
                if cart_item.quantity > cart_item.item.stock:
                    return False, f"Not enough stock for {cart_item.item.name}"
                
                # Update Stock
                item = cart_item.item
                item.stock -= cart_item.quantity
                item.save()
                summary_list.append(f"{cart_item.quantity}x {item.name}")

            # Update Profile Gold
            profile.gold -= total_cost
            profile.save()

            # Create Order Record
            Order.objects.create(
                user=self.user,
                total_gold=total_cost,
                summary=", ".join(summary_list)
            )

            # Delete Cart
            self.delete()
            return True, "Success"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.item.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"
    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now_add=True)
    total_gold = models.PositiveIntegerField()
    # A simple text field to store what was bought (snapshot)
    summary = models.TextField() 

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"