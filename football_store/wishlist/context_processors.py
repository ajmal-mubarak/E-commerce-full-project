from wishlist.utils import get_or_create_wishlist

def wishlist_count(request):
    if request.user.is_authenticated:
        wishlist = get_or_create_wishlist(request.user)
        return {'wishlist_count': wishlist.items.count()}
    return {'wishlist_count': 0}
