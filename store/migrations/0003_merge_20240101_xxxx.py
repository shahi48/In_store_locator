from django.db import migrations
from django.db.models import F

def update_product_data(apps, schema_editor):
    Product = apps.get_model('store', 'Product')
    
    product_updates = {
        'Atta': {
            'price': 350,
            'description': 'Premium quality wheat flour, perfect for making rotis and parathas. Finely ground and rich in nutrients.'
        },
        'Rice': {
            'price': 450,
            'description': 'Premium Basmati rice with long grains. Aromatic and perfect for biryani and pulao.'
        },
        'Dal': {
            'price': 180,
            'description': 'High-quality Toor Dal, essential for everyday Indian cooking. Rich in protein and nutrients.'
        },
        'Sugar': {
            'price': 45,
            'description': 'Fine grain pure sugar, perfect for your daily tea, coffee, and cooking needs.'
        },
        'Salt': {
            'price': 25,
            'description': 'Iodized table salt, essential for cooking and seasoning. Pure and fine quality.'
        },
        'Mobile Phone': {
            'price': 15999,
            'description': 'Feature-rich smartphone with 6GB RAM, 128GB storage, and powerful camera system.'
        },
        'Laptop': {
            'price': 45999,
            'description': 'High-performance laptop with Intel Core i5, 8GB RAM, and 512GB SSD storage.'
        },
        'Headphones': {
            'price': 1999,
            'description': 'Wireless Bluetooth headphones with noise cancellation and long battery life.'
        },
        'Smart Watch': {
            'price': 3499,
            'description': 'Fitness tracker with heart rate monitor, sleep tracking, and smartphone notifications.'
        },
        'T-Shirt': {
            'price': 599,
            'description': 'Pure cotton comfortable t-shirt, available in multiple colors and sizes.'
        },
        'Jeans': {
            'price': 1299,
            'description': 'Durable denim jeans with perfect fit and comfort. Premium quality material.'
        },
        'Shirt': {
            'price': 899,
            'description': 'Formal cotton shirt, wrinkle-resistant and perfect for office wear.'
        },
        'Kurta': {
            'price': 799,
            'description': 'Traditional Indian kurta with modern design. Pure cotton comfort.'
        },
        'Pressure Cooker': {
            'price': 1499,
            'description': 'Durable stainless steel pressure cooker, perfect for Indian cooking.'
        },
        'Tawa': {
            'price': 699,
            'description': 'Non-stick tawa for making rotis, dosas, and parathas. Even heating distribution.'
        },
        'Mixer Grinder': {
            'price': 2999,
            'description': 'Powerful 750W mixer grinder with 3 jars. Perfect for Indian cooking needs.'
        },
        'Gas Stove': {
            'price': 3499,
            'description': 'Efficient 3-burner gas stove with brass burners and high-quality build.'
        },
        'Shampoo': {
            'price': 299,
            'description': 'Nourishing shampoo with natural ingredients for healthy, shiny hair.'
        },
        'Soap': {
            'price': 45,
            'description': 'Gentle bathing soap with natural ingredients and refreshing fragrance.'
        },
        'Face Wash': {
            'price': 199,
            'description': 'Deep cleansing face wash suitable for all skin types.'
        },
        'Hand Sanitizer': {
            'price': 99,
            'description': '70% alcohol-based sanitizer with moisturizing properties.'
        }
    }

    for product_name, data in product_updates.items():
        Product.objects.filter(name__iexact=product_name).update(
            price=data['price'],
            description=data['description']
        )

def reverse_migration(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('store', '0002_alter_category_options'),  # First parent
        ('store', 'XXXX_update_product_prices_descriptions'),  # Second parent
    ]

    operations = [
        migrations.RunPython(update_product_data, reverse_migration),
    ] 