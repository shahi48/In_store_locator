from django.core.management.base import BaseCommand
from store.models import Category, Product
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populate database with sample categories and products'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Category.objects.all().delete()
        Product.objects.all().delete()

        # Create Categories with more products
        categories_data = [
            {
                "name": "Electronics",
                "description": "Electronic devices and accessories",
                "icon": "laptop",
                "products": [
                    {"name": "Smart TV 55\"", "price": "699.99", "aisle": "E1", "shelf": "S1"},
                    {"name": "Wireless Headphones", "price": "89.99", "aisle": "E1", "shelf": "S2"},
                    {"name": "Gaming Laptop", "price": "1299.99", "aisle": "E1", "shelf": "S3"},
                    {"name": "Smartphone", "price": "599.99", "aisle": "E2", "shelf": "S1"},
                    {"name": "Tablet", "price": "449.99", "aisle": "E2", "shelf": "S2"},
                    {"name": "Smartwatch", "price": "199.99", "aisle": "E2", "shelf": "S3"},
                    {"name": "Bluetooth Speaker", "price": "79.99", "aisle": "E3", "shelf": "S1"},
                    {"name": "Wireless Mouse", "price": "29.99", "aisle": "E3", "shelf": "S2"},
                    {"name": "Keyboard", "price": "49.99", "aisle": "E3", "shelf": "S3"},
                    {"name": "Monitor 27\"", "price": "299.99", "aisle": "E4", "shelf": "S1"}
                ]
            },
            {
                "name": "Groceries",
                "description": "Fresh food and pantry items",
                "icon": "shopping-basket",
                "products": [
                    {"name": "Organic Bananas", "price": "2.99", "aisle": "G1", "shelf": "S1"},
                    {"name": "Fresh Milk", "price": "3.49", "aisle": "G1", "shelf": "S2"},
                    {"name": "Whole Grain Bread", "price": "4.99", "aisle": "G2", "shelf": "S1"},
                    {"name": "Organic Eggs", "price": "5.99", "aisle": "G2", "shelf": "S2"},
                    {"name": "Greek Yogurt", "price": "4.49", "aisle": "G3", "shelf": "S1"},
                    {"name": "Fresh Spinach", "price": "2.99", "aisle": "G3", "shelf": "S2"},
                    {"name": "Chicken Breast", "price": "8.99", "aisle": "G4", "shelf": "S1"},
                    {"name": "Salmon Fillet", "price": "12.99", "aisle": "G4", "shelf": "S2"},
                    {"name": "Pasta", "price": "1.99", "aisle": "G5", "shelf": "S1"},
                    {"name": "Tomato Sauce", "price": "2.49", "aisle": "G5", "shelf": "S2"}
                ]
            },
            {
                "name": "Fashion",
                "description": "Clothing and accessories",
                "icon": "tshirt",
                "products": [
                    {"name": "Men's Jeans", "price": "49.99", "aisle": "F1", "shelf": "S1"},
                    {"name": "Women's Dress", "price": "79.99", "aisle": "F1", "shelf": "S2"},
                    {"name": "Running Shoes", "price": "89.99", "aisle": "F2", "shelf": "S1"},
                    {"name": "Leather Wallet", "price": "29.99", "aisle": "F2", "shelf": "S2"},
                    {"name": "Sunglasses", "price": "39.99", "aisle": "F3", "shelf": "S1"},
                    {"name": "Winter Jacket", "price": "129.99", "aisle": "F3", "shelf": "S2"},
                    {"name": "Cotton T-Shirt", "price": "19.99", "aisle": "F4", "shelf": "S1"},
                    {"name": "Yoga Pants", "price": "44.99", "aisle": "F4", "shelf": "S2"},
                    {"name": "Baseball Cap", "price": "24.99", "aisle": "F5", "shelf": "S1"},
                    {"name": "Leather Belt", "price": "34.99", "aisle": "F5", "shelf": "S2"}
                ]
            },
            {
                "name": "Home & Kitchen",
                "description": "Household items and appliances",
                "icon": "home",
                "products": [
                    {"name": "Coffee Maker", "price": "79.99", "aisle": "H1", "shelf": "S1"},
                    {"name": "Bed Sheets Set", "price": "49.99", "aisle": "H1", "shelf": "S2"},
                    {"name": "Kitchen Mixer", "price": "199.99", "aisle": "H2", "shelf": "S1"},
                    {"name": "Towel Set", "price": "34.99", "aisle": "H2", "shelf": "S2"},
                    {"name": "Blender", "price": "69.99", "aisle": "H3", "shelf": "S1"},
                    {"name": "Toaster", "price": "39.99", "aisle": "H3", "shelf": "S2"},
                    {"name": "Vacuum Cleaner", "price": "149.99", "aisle": "H4", "shelf": "S1"},
                    {"name": "Air Purifier", "price": "129.99", "aisle": "H4", "shelf": "S2"},
                    {"name": "Dining Set", "price": "199.99", "aisle": "H5", "shelf": "S1"},
                    {"name": "Cookware Set", "price": "159.99", "aisle": "H5", "shelf": "S2"}
                ]
            },
            {
                "name": "Sports & Outdoors",
                "description": "Sports equipment and outdoor gear",
                "icon": "basketball-ball",
                "products": [
                    {"name": "Yoga Mat", "price": "29.99", "aisle": "S1", "shelf": "S1"},
                    {"name": "Tennis Racket", "price": "89.99", "aisle": "S1", "shelf": "S2"},
                    {"name": "Camping Tent", "price": "199.99", "aisle": "S2", "shelf": "S1"},
                    {"name": "Hiking Boots", "price": "129.99", "aisle": "S2", "shelf": "S2"},
                    {"name": "Basketball", "price": "24.99", "aisle": "S3", "shelf": "S1"},
                    {"name": "Fitness Tracker", "price": "79.99", "aisle": "S3", "shelf": "S2"},
                    {"name": "Dumbbells Set", "price": "89.99", "aisle": "S4", "shelf": "S1"},
                    {"name": "Bicycle", "price": "299.99", "aisle": "S4", "shelf": "S2"},
                    {"name": "Swimming Goggles", "price": "19.99", "aisle": "S5", "shelf": "S1"},
                    {"name": "Soccer Ball", "price": "29.99", "aisle": "S5", "shelf": "S2"}
                ]
            },
            {
                "name": "Beauty & Personal Care",
                "description": "Cosmetics and personal care items",
                "icon": "spa",
                "products": [
                    {"name": "Face Moisturizer", "price": "24.99", "aisle": "B1", "shelf": "S1"},
                    {"name": "Shampoo Set", "price": "19.99", "aisle": "B1", "shelf": "S2"},
                    {"name": "Perfume", "price": "79.99", "aisle": "B2", "shelf": "S1"},
                    {"name": "Electric Toothbrush", "price": "89.99", "aisle": "B2", "shelf": "S2"},
                    {"name": "Hair Dryer", "price": "49.99", "aisle": "B3", "shelf": "S1"},
                    {"name": "Makeup Kit", "price": "59.99", "aisle": "B3", "shelf": "S2"},
                    {"name": "Face Mask Set", "price": "29.99", "aisle": "B4", "shelf": "S1"},
                    {"name": "Nail Polish Set", "price": "34.99", "aisle": "B4", "shelf": "S2"},
                    {"name": "Body Lotion", "price": "14.99", "aisle": "B5", "shelf": "S1"},
                    {"name": "Sunscreen", "price": "19.99", "aisle": "B5", "shelf": "S2"}
                ]
            },
            {
                "name": "Books & Stationery",
                "description": "Books, notebooks, and office supplies",
                "icon": "book",
                "products": [
                    {"name": "Bestseller Novel", "price": "19.99", "aisle": "L1", "shelf": "S1"},
                    {"name": "Notebook Set", "price": "12.99", "aisle": "L1", "shelf": "S2"},
                    {"name": "Art Supplies Kit", "price": "39.99", "aisle": "L2", "shelf": "S1"},
                    {"name": "Desk Organizer", "price": "24.99", "aisle": "L2", "shelf": "S2"},
                    {"name": "Planner 2024", "price": "16.99", "aisle": "L3", "shelf": "S1"},
                    {"name": "Pen Set", "price": "9.99", "aisle": "L3", "shelf": "S2"},
                    {"name": "Sketchbook", "price": "14.99", "aisle": "L4", "shelf": "S1"},
                    {"name": "Colored Pencils", "price": "19.99", "aisle": "L4", "shelf": "S2"},
                    {"name": "Bookmarks Set", "price": "7.99", "aisle": "L5", "shelf": "S1"},
                    {"name": "Reading Light", "price": "15.99", "aisle": "L5", "shelf": "S2"}
                ]
            },
            {
                "name": "Toys & Games",
                "description": "Children's toys and board games",
                "icon": "gamepad",
                "products": [
                    {"name": "Board Game Set", "price": "29.99", "aisle": "T1", "shelf": "S1"},
                    {"name": "LEGO Kit", "price": "59.99", "aisle": "T1", "shelf": "S2"},
                    {"name": "RC Car", "price": "89.99", "aisle": "T2", "shelf": "S1"},
                    {"name": "Stuffed Animal", "price": "19.99", "aisle": "T2", "shelf": "S2"},
                    {"name": "Puzzle Set", "price": "24.99", "aisle": "T3", "shelf": "S1"},
                    {"name": "Art & Craft Kit", "price": "34.99", "aisle": "T3", "shelf": "S2"},
                    {"name": "Building Blocks", "price": "44.99", "aisle": "T4", "shelf": "S1"},
                    {"name": "Doll House", "price": "79.99", "aisle": "T4", "shelf": "S2"},
                    {"name": "Science Kit", "price": "39.99", "aisle": "T5", "shelf": "S1"},
                    {"name": "Card Games", "price": "14.99", "aisle": "T5", "shelf": "S2"}
                ]
            }
        ]

        # Create categories and products
        for cat_data in categories_data:
            category = Category.objects.create(
                name=cat_data["name"],
                description=cat_data["description"]
            )
            
            # Create products for this category
            for prod_data in cat_data["products"]:
                Product.objects.create(
                    name=prod_data["name"],
                    description=f"High-quality {prod_data['name'].lower()} in our {cat_data['name']} section",
                    price=Decimal(prod_data["price"]),
                    category=category,
                    aisle=prod_data["aisle"],
                    shelf=prod_data["shelf"]
                )

        self.stdout.write(self.style.SUCCESS(f'Successfully created {Category.objects.count()} categories and {Product.objects.count()} products')) 