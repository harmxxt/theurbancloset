"""
Seed command for TheUrbanCloset luxury products.
Products are assigned to BOTH a gender category AND a type category
so that:
  - Men's page shows all men's clothing
  - Women's page shows all women's clothing
  - Shirts page shows all shirts (men's)
  - Dresses page shows all dresses (women's)
  - etc.

We achieve this by assigning each product to its most specific category
(shirts, dresses, jackets, etc.) and then using the category_products view
to show men/women by filtering across multiple subcategories.
"""

from django.core.management.base import BaseCommand
from products.models import Category, Product


class Command(BaseCommand):
    help = 'Seed TheUrbanCloset luxury products across all categories'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding TheUrbanCloset products...')

        cats_data = [
            {'name': 'Men',         'slug': 'men',         'color': '#1A1A1A'},
            {'name': 'Women',       'slug': 'women',       'color': '#C9A96E'},
            {'name': 'Shirts',      'slug': 'shirts',      'color': '#2C5F8A'},
            {'name': 'T-Shirts',    'slug': 't-shirts',    'color': '#4A7C59'},
            {'name': 'Jackets',     'slug': 'jackets',     'color': '#8B4513'},
            {'name': 'Dresses',     'slug': 'dresses',     'color': '#C9A96E'},
            {'name': 'Shoes',       'slug': 'shoes',       'color': '#333333'},
            {'name': 'Accessories', 'slug': 'accessories', 'color': '#9B59B6'},
        ]

        cats = {}
        for cd in cats_data:
            cat, created = Category.objects.get_or_create(
                slug=cd['slug'],
                defaults={'name': cd['name'], 'color': cd['color']}
            )
            cats[cd['slug']] = cat
            if created:
                self.stdout.write(f'  + Category: {cat.name}')

        products = [

            # ── SHIRTS (Men) ───────────────────────────────────────────
            {
                'name': 'Obsidian Premium Cotton Shirt',
                'slug': 'obsidian-premium-cotton-shirt',
                'category': 'shirts',
                'description': 'Crafted from the finest Egyptian cotton with a slim-fit silhouette, mother-of-pearl buttons and double-stitched seams. The definitive dress shirt for the modern man.',
                'price': 4999, 'discount_price': 3999, 'stock': 25,
                'sizes': 'S,M,L,XL,XXL', 'material': '100% Egyptian Cotton',
                'image_url': 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=600&q=80',
                'is_featured': True,
            },
            {
                'name': 'Midnight Velour Dress Shirt',
                'slug': 'midnight-velour-dress-shirt',
                'category': 'shirts',
                'description': 'A refined dress shirt with an ultra-smooth Supima cotton finish, spread collar and French cuffs. Built for the boardroom and the black-tie event alike.',
                'price': 5999, 'stock': 18,
                'sizes': 'S,M,L,XL', 'material': 'Supima Cotton',
                'image_url': 'https://images.unsplash.com/photo-1620012253295-c15cc3e65df4?w=600&q=80',
                'is_featured': False,
            },
            {
                'name': 'Royal Blue Linen Shirt',
                'slug': 'royal-blue-linen-shirt',
                'category': 'shirts',
                'description': 'Relaxed-fit pure linen shirt in deep royal blue. Breathable and cool for warm days, with a classic button-down collar.',
                'price': 3499, 'stock': 28,
                'sizes': 'S,M,L,XL,XXL', 'material': 'Pure Linen',
                'image_url': 'https://images.unsplash.com/photo-1607345366928-199ea26cfe3e?w=600&q=80',
                'is_featured': False,
            },
            {
                'name': 'Ivory Classic Oxford Shirt',
                'slug': 'ivory-classic-oxford-shirt',
                'category': 'shirts',
                'description': 'A timeless ivory Oxford-weave shirt with a button-down collar and box pleat back. Effortless versatility from desk to dinner.',
                'price': 3999, 'stock': 22,
                'sizes': 'S,M,L,XL,XXL', 'material': 'Oxford Cotton',
                'image_url': 'https://images.unsplash.com/photo-1602810319428-019690571b5b?w=600&q=80',
                'is_featured': False,
            },

            # ── T-SHIRTS (Men) ──────────────────────────────────────────
            {
                'name': 'Graphite Merino T-Shirt',
                'slug': 'graphite-merino-tshirt',
                'category': 't-shirts',
                'description': 'Premium crew-neck T-shirt in ultra-fine merino wool. Naturally temperature-regulating, odor-resistant and breathable for all-day wear.',
                'price': 2499, 'discount_price': 1999, 'stock': 40,
                'sizes': 'XS,S,M,L,XL,XXL', 'material': 'Ultra-fine Merino Wool',
                'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=600&q=80',
                'is_featured': False,
            },
            {
                'name': 'White Pima Cotton Essential Tee',
                'slug': 'white-pima-cotton-tee',
                'category': 't-shirts',
                'description': 'The perfect white T-shirt, reimagined in Peruvian Pima cotton. Incomparable softness with a relaxed, confident fit.',
                'price': 1999, 'stock': 55,
                'sizes': 'XS,S,M,L,XL,XXL', 'material': 'Peruvian Pima Cotton',
                'image_url': 'https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=600&q=80',
                'is_featured': False,
            },
            {
                'name': 'Essential Black Polo',
                'slug': 'essential-black-polo',
                'category': 't-shirts',
                'description': 'Luxury polo in piqué cotton with a refined three-button placket. The cornerstone of every smart-casual wardrobe.',
                'price': 2999, 'stock': 35,
                'sizes': 'S,M,L,XL,XXL', 'material': 'Piqué Cotton',
                'image_url': 'https://images.unsplash.com/photo-1574180045827-681f8a1a9622?w=600&q=80',
                'is_featured': False,
            },
            {
                'name': 'Navy Stripe Breton Tee',
                'slug': 'navy-stripe-breton-tee',
                'category': 't-shirts',
                'description': 'A classic Breton-stripe tee in navy and white, cut from soft brushed jersey. Relaxed nautical style for casual weekends.',
                'price': 2199, 'stock': 30,
                'sizes': 'XS,S,M,L,XL', 'material': 'Brushed Cotton Jersey',
                'image_url': 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=600&q=80',
                'is_featured': False,
            },

            # ── JACKETS (Men + Women) ───────────────────────────────────
            {
                'name': 'The Baron Wool Blazer',
                'slug': 'baron-wool-blazer',
                'category': 'jackets',
                'description': 'A masterfully tailored single-breasted blazer in 100% Italian wool. Notch lapels, functional button cuffs and a perfectly structured shoulder.',
                'price': 18999, 'discount_price': 15999, 'stock': 12,
                'sizes': 'S,M,L,XL,XXL', 'material': 'Italian Merino Wool',
                'image_url': 'https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=600&q=80',
                'is_featured': True,
            },
            {
                'name': 'Noir Leather Biker Jacket',
                'slug': 'noir-leather-biker-jacket',
                'category': 'jackets',
                'description': 'Full-grain Italian leather jacket with asymmetric zip closure, quilted shoulder panels and chrome hardware. Effortless luxury.',
                'price': 32999, 'stock': 8,
                'sizes': 'S,M,L,XL', 'material': 'Full-grain Italian Leather',
                'image_url': 'https://images.unsplash.com/photo-1520975954732-35dd22299614?w=600&q=80',
                'is_featured': True,
            },
            {
                'name': 'Cashmere Oversized Blazer',
                'slug': 'cashmere-oversized-blazer',
                'category': 'jackets',
                'description': 'Softly structured blazer in 100% grade-A cashmere with a relaxed oversized fit. For women who wear power lightly.',
                'price': 22999, 'discount_price': 18999, 'stock': 14,
                'sizes': 'XS,S,M,L,XL', 'material': 'Grade-A Cashmere',
                'image_url': 'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=600&q=80',
                'is_featured': True,
            },
            {
                'name': 'Camel Wool Overcoat',
                'slug': 'camel-wool-overcoat',
                'category': 'jackets',
                'description': 'A heritage camel-tone wool overcoat with a double-breasted front and structured shoulders. Investment dressing at its finest.',
                'price': 27999, 'stock': 9,
                'sizes': 'S,M,L,XL', 'material': 'Wool Blend',
                'image_url': 'https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=600&q=80',
                'is_featured': False,
            },

            # ── DRESSES (Women) ─────────────────────────────────────────
            {
                'name': 'Ivory Silk Maxi Dress',
                'slug': 'ivory-silk-maxi-dress',
                'category': 'dresses',
                'description': 'A fluid ivory silk maxi dress with a draped cowl neckline and side slit. Hand-finished with silk thread for a luxurious drape.',
                'price': 14999, 'discount_price': 12499, 'stock': 15,
                'sizes': 'XS,S,M,L,XL', 'material': '100% Mulberry Silk',
                'image_url': 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=600&q=80',
                'is_featured': True,
            },
            {
                'name': 'Midnight Velvet Evening Dress',
                'slug': 'midnight-velvet-evening-dress',
                'category': 'dresses',
                'description': 'A deep midnight blue velvet slip dress with thin shoulder straps and a bias-cut silhouette. Old-world glamour for modern evenings.',
                'price': 19999, 'stock': 10,
                'sizes': 'XS,S,M,L', 'material': 'Crushed Velvet',
                'image_url': 'https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=600&q=80',
                'is_featured': True,
            },
            {
                'name': 'Blush Linen Co-ord Set',
                'slug': 'blush-linen-coord-set',
                'category': 'dresses',
                'description': 'A relaxed blush-pink linen crop top and wide-leg trouser set. Effortlessly chic for brunch, travel or a leisurely afternoon.',
                'price': 8999, 'discount_price': 7499, 'stock': 20,
                'sizes': 'XS,S,M,L,XL', 'material': 'Pure Linen',
                'image_url': 'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=600&q=80',
                'is_featured': True,
            },
            {
                'name': 'White Broderie Anglaise Dress',
                'slug': 'white-broderie-anglaise-dress',
                'category': 'dresses',
                'description': 'A romantic white midi dress with delicate broderie anglaise detailing, square neckline and flutter sleeves.',
                'price': 9499, 'stock': 18,
                'sizes': 'XS,S,M,L', 'material': 'Cotton Broderie',
                'image_url': 'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=600&q=80',
                'is_featured': False,
            },
            {
                'name': 'Terracotta Wrap Midi Dress',
                'slug': 'terracotta-wrap-midi-dress',
                'category': 'dresses',
                'description': 'A flattering wrap-style midi dress in warm terracotta crepe. Adjustable tie waist and V-neckline for an effortlessly elegant silhouette.',
                'price': 7999, 'stock': 22,
                'sizes': 'XS,S,M,L,XL', 'material': 'Viscose Crepe',
                'image_url': 'https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=600&q=80',
                'is_featured': False,
            },

            # ── SHOES ───────────────────────────────────────────────────
            {
                'name': 'Oxford Derby in Cognac',
                'slug': 'oxford-derby-cognac',
                'category': 'shoes',
                'description': 'Hand-welted Oxford shoes in cognac full-grain leather with Goodyear construction. They age beautifully with every wear.',
                'price': 24999, 'discount_price': 21999, 'stock': 10,
                'sizes': '6,7,8,9,10,11,12', 'material': 'Full-grain Cognac Leather',
                'image_url': 'https://images.unsplash.com/photo-1449505278894-297fdb3edbc1?w=600&q=80',
                'is_featured': True,
            },
            {
                'name': 'Gold Strappy Heeled Sandals',
                'slug': 'gold-strappy-heeled-sandals',
                'category': 'shoes',
                'description': 'Delicate gold metallic leather sandals with thin adjustable straps and a sculpted 7cm heel. The ultimate elevated party shoe.',
                'price': 11999, 'stock': 20,
                'sizes': '5,6,7,8,9,10', 'material': 'Metallic Leather',
                'image_url': 'https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=600&q=80',
                'is_featured': False,
            },
            {
                'name': 'White Leather Minimal Sneakers',
                'slug': 'white-leather-minimal-sneakers',
                'category': 'shoes',
                'description': 'Clean, low-profile leather sneakers with a cupsole and tonal laces. The everyday shoe that goes with everything.',
                'price': 8499, 'discount_price': 6999, 'stock': 32,
                'sizes': '5,6,7,8,9,10,11,12', 'material': 'Full-grain Leather',
                'image_url': 'https://images.unsplash.com/photo-1560769629-975ec94e6a86?w=600&q=80',
                'is_featured': False,
            },
            {
                'name': 'Black Chelsea Ankle Boots',
                'slug': 'black-chelsea-ankle-boots',
                'category': 'shoes',
                'description': 'Classic pull-on Chelsea boots in smooth black leather with elasticated side panels and a stacked leather heel.',
                'price': 15999, 'stock': 14,
                'sizes': '5,6,7,8,9,10,11', 'material': 'Smooth Calf Leather',
                'image_url': 'https://images.unsplash.com/photo-1638247025967-b4e38f787b76?w=600&q=80',
                'is_featured': False,
            },

            # ── ACCESSORIES ─────────────────────────────────────────────
            {
                'name': "Classic Gold Watch",
                'slug': 'mens-classic-watch-gold',
                'category': 'accessories',
                'description': 'Swiss-movement timepiece with a gold-tone stainless steel case, white enamel dial and genuine leather strap.',
                'price': 29999, 'stock': 5,
                'sizes': 'One Size', 'material': 'Stainless Steel & Leather',
                'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&q=80',
                'is_featured': True,
            },
            {
                'name': 'Artisan Leather Belt — Black',
                'slug': 'artisan-leather-belt-black',
                'category': 'accessories',
                'description': 'Full-grain vegetable-tanned leather belt with a brushed silver buckle. Develops a beautiful patina over time.',
                'price': 3999, 'stock': 30,
                'sizes': 'S,M,L,XL', 'material': 'Vegetable-tanned Leather',
                'image_url': 'https://images.unsplash.com/photo-1624222247344-550fb60583dc?w=600&q=80',
                'is_featured': False,
            },
            {
                'name': 'Amber Tortoiseshell Sunglasses',
                'slug': 'amber-tortoiseshell-sunglasses',
                'category': 'accessories',
                'description': 'Handcrafted Italian acetate frames in warm amber tortoiseshell with polarized UV400 lenses.',
                'price': 8499, 'discount_price': 6999, 'stock': 22,
                'sizes': 'One Size', 'material': 'Italian Acetate',
                'image_url': 'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=600&q=80',
                'is_featured': False,
            },
            {
                'name': 'Silk Pocket Square — Noir',
                'slug': 'silk-pocket-square-noir',
                'category': 'accessories',
                'description': 'A hand-rolled silk pocket square in lustrous black with an ivory border. The perfect finishing detail for any formal ensemble.',
                'price': 1299, 'stock': 60,
                'sizes': 'One Size', 'material': '100% Silk',
                'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600&q=80',
                'is_featured': False,
            },
            {
                'name': 'Structured Leather Tote Bag',
                'slug': 'structured-leather-tote-bag',
                'category': 'accessories',
                'description': 'A clean-lined tote bag in pebbled tan leather with a suede interior, gold hardware and detachable pouch.',
                'price': 18999, 'discount_price': 15999, 'stock': 12,
                'sizes': 'One Size', 'material': 'Pebbled Leather',
                'image_url': 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600&q=80',
                'is_featured': True,
            },
        ]

        # ── Map subcategory → gender for the Men/Women pages ──────────
        # Men's page shows: shirts, t-shirts, men's jackets/shoes
        # Women's page shows: dresses, women's jackets/shoes
        # We do this by ALSO creating a second product entry under men/women
        # for the "All Men's" and "All Women's" filtered views.
        #
        # Simpler approach: category_products view queries subcategories.

        created = updated = 0
        for p in products:
            cat_slug = p.pop('category')
            product, is_new = Product.objects.update_or_create(
                slug=p['slug'],
                defaults={**p, 'category': cats[cat_slug], 'brand': 'TheUrbanCloset'}
            )
            if is_new:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f'\n✓ Done! {created} created, {updated} updated across all categories.'
        ))
