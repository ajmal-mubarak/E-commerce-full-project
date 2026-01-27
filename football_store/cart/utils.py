import uuid
from .models import Cart, CartItem
from django.contrib.auth.models import User


def get_or_create_session_cart(request):
    session_id = request.session.get("session_id")

    if not session_id:
        session_id = str(uuid.uuid4())
        request.session["session_id"] = session_id

    cart, created = Cart.objects.get_or_create(session_id=session_id, user=None)
    return cart


def get_or_create_user_cart(user):
    cart, created = Cart.objects.get_or_create(user=user, session_id=None)
    return cart


def merge_session_cart_to_user(request, user):
    try:
        session_id = request.session.get("session_id")
        if not session_id:
            return

        session_cart = Cart.objects.filter(session_id=session_id, user=None).first()
        if not session_cart:
            return

        user_cart = get_or_create_user_cart(user)

        for item in session_cart.items.all():
            existing_item = user_cart.items.filter(product=item.product).first()
            if existing_item:
                existing_item.quantity += item.quantity
                existing_item.save()
            else:
                item.cart = user_cart
                item.save()

        session_cart.delete()
        del request.session["session_id"]

    except:
        pass
