"""Tests for services."""

import pytest
from sqlalchemy.orm import Session
from core.database import SessionLocal, init_db, drop_db
from memory import ProductSchema, CustomerSchema
from services import InventoryService, CustomerService


@pytest.fixture
def db_session():
    """Create a test database session."""
    init_db()
    db = SessionLocal()
    yield db
    db.close()
    drop_db()


def test_create_product(db_session: Session):
    """Test creating a product."""
    service = InventoryService(db_session)
    
    product_data = ProductSchema(
        name="Test Product",
        description="A test product",
        price=100.0,
        quantity=50,
        reorder_level=10,
        supplier="Test Supplier",
        category="Test Category",
    )
    
    product = service.create_product(product_data)
    assert product.name == "Test Product"
    assert product.price == 100.0
    assert product.quantity == 50


def test_get_product(db_session: Session):
    """Test retrieving a product."""
    service = InventoryService(db_session)
    
    product_data = ProductSchema(
        name="Test Product",
        price=100.0,
        quantity=50,
    )
    
    created = service.create_product(product_data)
    retrieved = service.get_product(created.id)
    
    assert retrieved is not None
    assert retrieved.name == "Test Product"


def test_add_stock(db_session: Session):
    """Test adding stock to a product."""
    service = InventoryService(db_session)
    
    product_data = ProductSchema(
        name="Test Product",
        price=100.0,
        quantity=50,
    )
    
    created = service.create_product(product_data)
    updated = service.add_stock(created.id, 20)
    
    assert updated.quantity == 70


def test_create_customer(db_session: Session):
    """Test creating a customer."""
    service = CustomerService(db_session)
    
    customer_data = CustomerSchema(
        name="Test Customer",
        email="test@example.com",
        phone="1234567890",
    )
    
    customer = service.create_customer(customer_data)
    assert customer.name == "Test Customer"
    assert customer.email == "test@example.com"
