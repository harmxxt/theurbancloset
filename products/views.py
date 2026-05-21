from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category

# Men page shows shirts + t-shirts (strictly menswear)
MEN_SLUGS   = ['shirts', 't-shirts']
# Women page shows dresses (strictly womenswear)
WOMEN_SLUGS = ['dresses']
# jackets, shoes, accessories have their own unisex pages


def _sidebar_counts():
    """
    Returns {slug: count} for sidebar display.
    Men/Women use aggregated counts to match what their pages actually show.
    """
    counts = {}
    for cat in Category.objects.all():
        counts[cat.slug] = Product.objects.filter(
            category=cat, is_active=True
        ).count()
    counts['men']   = Product.objects.filter(is_active=True, category__slug__in=MEN_SLUGS).count()
    counts['women'] = Product.objects.filter(is_active=True, category__slug__in=WOMEN_SLUGS).count()
    return counts


def _apply_sort(qs, sort):
    mapping = {
        'price_low':  'price',
        'price_high': '-price',
        'name':       'name',
    }
    return qs.order_by(mapping.get(sort, '-created_at'))


def home(request):
    featured     = Product.objects.filter(is_active=True, is_featured=True)[:8]
    new_arrivals = Product.objects.filter(is_active=True).order_by('-created_at')[:4]
    categories   = Category.objects.all()
    return render(request, 'products/home.html', {
        'featured_products': featured,
        'new_arrivals':      new_arrivals,
        'categories':        categories,
    })


def product_list(request):
    products   = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    selected_category = None
    query = request.GET.get('q', '').strip()
    sort  = request.GET.get('sort', 'newest')

    cat_slug = request.GET.get('category')
    if cat_slug:
        selected_category = get_object_or_404(Category, slug=cat_slug)
        products = products.filter(category=selected_category)

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

    products    = _apply_sort(products, sort)
    counts      = _sidebar_counts()
    total_count = Product.objects.filter(is_active=True).count()

    return render(request, 'products/product_list.html', {
        'products':          products,
        'categories':        categories,
        'selected_category': selected_category,
        'query':             query,
        'sort':              sort,
        'counts':            counts,
        'total_count':       total_count,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(id=product.id)[:4]
    return render(request, 'products/product_detail.html', {
        'product':          product,
        'related_products': related,
        'sizes':            product.get_sizes_list(),
    })


def category_products(request, slug):
    category   = get_object_or_404(Category, slug=slug)
    categories = Category.objects.all()
    sort       = request.GET.get('sort', 'newest')

    if slug == 'men':
        products = Product.objects.filter(is_active=True, category__slug__in=MEN_SLUGS)
    elif slug == 'women':
        products = Product.objects.filter(is_active=True, category__slug__in=WOMEN_SLUGS)
    else:
        products = Product.objects.filter(category=category, is_active=True)

    products    = _apply_sort(products, sort)
    counts      = _sidebar_counts()
    total_count = Product.objects.filter(is_active=True).count()

    return render(request, 'products/product_list.html', {
        'products':          products,
        'categories':        categories,
        'selected_category': category,
        'sort':              sort,
        'query':             '',
        'counts':            counts,
        'total_count':       total_count,
    })
