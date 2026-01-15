"""Inventory service for product management."""

import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from core.logger import setup_logger
from memory import Product, ProductSchema

logger = setup_logger(__name__)


class InventoryService:
    """Service for managing product inventory."""

    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db

    def create_product(self, product: ProductSchema) -> Product:
        """Create a new product."""
        try:
            db_product = Product(
                id=str(uuid.uuid4()),
                name=product.name,
                description=product.description,
                price=product.price,
                quantity=product.quantity,
                reorder_level=product.reorder_level,
                supplier=product.supplier,
                category=product.category,
            )
            self.db.add(db_product)
            self.db.commit()
            self.db.refresh(db_product)
            logger.info(f"Created product: {db_product.name} (ID: {db_product.id})")
            return db_product
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating product: {e}")
            raise

    def get_product(self, product_id: str) -> Optional[Product]:
        """Get product by ID."""
        try:
            return self.db.query(Product).filter(Product.id == product_id).first()
        except Exception as e:
            logger.error(f"Error getting product {product_id}: {e}")
            return None

    def get_product_by_name(self, name: str) -> Optional[Product]:
        """Get product by name."""
        try:
            return self.db.query(Product).filter(
                Product.name.ilike(f"%{name}%")
            ).first()
        except Exception as e:
            logger.error(f"Error getting product by name {name}: {e}")
            return None

    def get_all_products(self, category: Optional[str] = None) -> List[Product]:
        """Get all products, optionally filtered by category."""
        try:
            query = self.db.query(Product)
            if category:
                query = query.filter(Product.category == category)
            return query.all()
        except Exception as e:
            logger.error(f"Error getting all products: {e}")
            return []

    def update_product(self, product_id: str, product: ProductSchema) -> Optional[Product]:
        """Update an existing product."""
        try:
            db_product = self.db.query(Product).filter(Product.id == product_id).first()
            if not db_product:
                logger.warning(f"Product not found: {product_id}")
                return None

            db_product.name = product.name
            db_product.description = product.description
            db_product.price = product.price
            db_product.quantity = product.quantity
            db_product.reorder_level = product.reorder_level
            db_product.supplier = product.supplier
            db_product.category = product.category

            self.db.commit()
            self.db.refresh(db_product)
            logger.info(f"Updated product: {product_id}")
            return db_product
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating product {product_id}: {e}")
            raise

    def add_stock(self, product_id: str, quantity: int) -> Optional[Product]:
        """Add to product stock."""
        try:
            db_product = self.db.query(Product).filter(Product.id == product_id).first()
            if not db_product:
                logger.warning(f"Product not found: {product_id}")
                return None

            db_product.quantity += quantity
            self.db.commit()
            self.db.refresh(db_product)
            logger.info(f"Added {quantity} units to {db_product.name}. New quantity: {db_product.quantity}")
            return db_product
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error adding stock to product {product_id}: {e}")
            raise

    def remove_stock(self, product_id: str, quantity: int) -> Optional[Product]:
        """Remove from product stock."""
        try:
            db_product = self.db.query(Product).filter(Product.id == product_id).first()
            if not db_product:
                logger.warning(f"Product not found: {product_id}")
                return None

            if db_product.quantity < quantity:
                logger.warning(f"Insufficient stock: {db_product.name}")
                raise ValueError(f"Insufficient stock for {db_product.name}")

            db_product.quantity -= quantity
            self.db.commit()
            self.db.refresh(db_product)
            logger.info(f"Removed {quantity} units from {db_product.name}. New quantity: {db_product.quantity}")
            return db_product
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error removing stock from product {product_id}: {e}")
            raise

    def get_low_stock_products(self) -> List[Product]:
        """Get products below reorder level."""
        try:
            return self.db.query(Product).filter(
                Product.quantity <= Product.reorder_level
            ).all()
        except Exception as e:
            logger.error(f"Error getting low stock products: {e}")
            return []

    def delete_product(self, product_id: str) -> bool:
        """Delete a product."""
        try:
            db_product = self.db.query(Product).filter(Product.id == product_id).first()
            if not db_product:
                logger.warning(f"Product not found: {product_id}")
                return False

            self.db.delete(db_product)
            self.db.commit()
            logger.info(f"Deleted product: {product_id}")
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deleting product {product_id}: {e}")
            raise
