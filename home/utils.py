import json
from .models import *

# Updated cookieCart function
def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES.get('cart', '{}'))
    except json.JSONDecodeError:
        cart = {}

    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cart_items = order['get_cart_items']

    for item_id, item_data in cart.items():
        try:
            quantity = item_data.get('quantity', 0)

            if quantity > 0:
                cart_items += quantity

                product = Items.objects.get(id=item_id)
                total = product.price * quantity

                order['get_cart_total'] += total
                order['get_cart_items'] += quantity

                item = {
                    'id': product.id,
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'image_url': product.image_url
                    },
                    'quantity': quantity,
                    'available_online': product.available_online,
                    'get_total': total,
                }
                items.append(item)

                if not product.available_online:
                    order['shipping'] = True
        except Items.DoesNotExist:
            pass

    return {'cartItems': cart_items, 'order': order, 'items': items}

# Updated cartData function
def cartData(request):
    if request.user.is_authenticated:
#        customer = request.user
#        order, created = Order.objects.get_or_create(customer=customer, complete=False)
#        items = order.orderitem_set.all()
#        cart_items = order.get_cart_items()
        cookie_data = cookieCart(request)
        cart_items = cookie_data['cartItems']
        order = cookie_data['order']
        items = cookie_data['items']
    else:
        cookie_data = cookieCart(request)
        cart_items = cookie_data['cartItems']
        order = cookie_data['order']
        items = cookie_data['items']

    return {'cartItems': cart_items, 'order': order, 'items': items}


def guestOrder(request, data):
    name = data['form']['name']
    email = data['form']['email']

    cookie_data = cookieCart(request)
    items = cookie_data['items']

    # Get or create a user with the provided email
    customer, created = Customer.objects.get_or_create(email=email)
    
    # Update the user's name
    customer.username = name
    customer.save()

    # Create an order for the customer
    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    # Add items to the order
    for item in items:
        try:
            product = Items.objects.get(id=item['id'])

            # Ensure quantity is non-negative
            quantity = max(item['quantity'], 0)

            order_item = OrderItem.objects.create(
                product=product,
                order=order,
                quantity=quantity,
            )
        except Items.DoesNotExist:
            pass

    return customer, order