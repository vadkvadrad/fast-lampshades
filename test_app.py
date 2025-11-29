"""
Simple test script to verify the application structure and functionality
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported without errors"""
    try:
        from app.main import app
        from app import models
        from app import schemas
        from app import auth
        from app.api import auth as auth_api
        from app.api import products
        from app.api import cart
        from app.api import orders
        print("✅ All modules imported successfully")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_models():
    """Test that models are defined correctly"""
    try:
        from app.models import User, Product, Cart, Order, OrderItem
        
        # Check that all models have expected attributes
        user_attrs = ['id', 'email', 'password_hash', 'created_at']
        for attr in user_attrs:
            assert hasattr(User, attr), f"User model missing {attr}"
        
        product_attrs = ['id', 'name', 'description', 'price', 'created_at']
        for attr in product_attrs:
            assert hasattr(Product, attr), f"Product model missing {attr}"
        
        print("✅ All models are defined correctly")
        return True
    except Exception as e:
        print(f"❌ Model error: {e}")
        return False

def test_schemas():
    """Test that schemas are defined correctly"""
    try:
        from app.schemas import (
            UserCreate, UserLogin, UserResponse,
            ProductCreate, ProductResponse,
            CartItemCreate, CartResponse,
            OrderCreate, OrderResponse, OrderDetailResponse
        )
        
        print("✅ All schemas are defined correctly")
        return True
    except Exception as e:
        print(f"❌ Schema error: {e}")
        return False

def main():
    print("Testing LampShades MVP Application...")
    print("="*50)
    
    all_tests_passed = True
    
    all_tests_passed &= test_imports()
    all_tests_passed &= test_models()
    all_tests_passed &= test_schemas()
    
    print("="*50)
    if all_tests_passed:
        print("🎉 All tests passed! The application is ready.")
    else:
        print("❌ Some tests failed!")
    
    return all_tests_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)