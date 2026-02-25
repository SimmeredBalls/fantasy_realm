from django.shortcuts import render
from .models import Item
from django.shortcuts import redirect, get_object_or_404
from .models import Item, Cart, CartItem, Order
from django.contrib import messages

def item_list(request):
    # Fetch all items from the database
    items = Item.objects.all()
    
    # Pass them to the 'shop_home.html' template
    return render(request, 'shop/shop_home.html', {'items': items})

def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    # Get the player's gold from their profile
    player_profile = request.user.profile 
    
    if player_profile.gold >= item.price:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        # Logic: We don't subtract the gold yet! 
        # Only subtract it during 'checkout'.
        return redirect('view_cart')
    else:
        # If they are too poor, just send them back (or add an error message)
        return redirect('home')

def view_cart(request):
    # Get the cart for the user, or None if they don't have one yet
    cart = Cart.objects.filter(user=request.user).first()
    return render(request, 'shop/cart.html', {'cart': cart})

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, cart__user=request.user, id=item_id)
    cart_item.delete()
    return redirect('view_cart')

def adjust_quantity(request, item_id, action):
    cart_item = get_object_or_404(CartItem, cart__user=request.user, id=item_id)
    
    if action == 'add':
        # Check if there is enough stock before increasing
        if cart_item.item.stock > cart_item.quantity:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.warning(request, f"The shopkeeper says: 'I don't have any more {cart_item.item.name}s!'")
            
    elif action == 'remove':
        cart_item.quantity -= 1
        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.save()
            
    return redirect('view_cart')

def checkout(request):
    if request.method == "POST":
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            success, message = cart.process_checkout() # All logic happens here now
            if success:
                return render(request, 'shop/success.html')
            else:
                messages.error(request, message)
                return redirect('view_cart')
    return redirect('home')

def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-ordered_at')
    return render(request, 'shop/orders.html', {'orders': orders})

