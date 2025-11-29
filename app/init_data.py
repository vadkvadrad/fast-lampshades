from app.database import SessionLocal
from app.models import Product

def initialize_sample_data():
    """Initialize the database with sample product data."""
    db = SessionLocal()
    try:
        # Check if products already exist
        existing_count = db.query(Product).count()
        if existing_count > 0:
            print("Sample data already exists, skipping initialization.")
            return
        
        # Create sample products
        sample_products = [
            Product(
                name='Classic Table Lamp',
                description='A beautiful classic table lamp with adjustable brightness',
                price=49.99
            ),
            Product(
                name='Modern Desk Lamp',
                description='Sleek modern design with LED lighting',
                price=39.99
            ),
            Product(
                name='Vintage Floor Lamp',
                description='Elegant vintage-style floor lamp',
                price=89.99
            ),
            Product(
                name='Minimalist Pendant Light',
                description='Simple yet stylish pendant light for modern homes',
                price=59.99
            ),
            Product(
                name='Rustic Bedside Lamp',
                description='Warm rustic charm for your bedroom',
                price=34.99
            ),
            Product(
                name='Industrial Pipe Lamp',
                description='Unique industrial design with exposed pipes',
                price=74.99
            ),
            Product(
                name='Smart RGB Desk Lamp',
                description='Color-changing smart lamp with app control',
                price=69.99
            ),
            Product(
                name='Art Deco Table Lamp',
                description='Luxurious art deco design with crystal details',
                price=99.99
            ),
        ]
        
        for product in sample_products:
            db.add(product)
        
        db.commit()
        print("Sample data initialized successfully.")
    except Exception as e:
        print(f"Error initializing sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    initialize_sample_data()