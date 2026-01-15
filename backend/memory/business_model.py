"""Business entity models and schemas."""

from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel, Field
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, Boolean
from sqlalchemy.types import JSON
from core.database import Base


# ============================================================================
# PYDANTIC SCHEMAS (for API requests/responses)
# ============================================================================


class ProductSchema(BaseModel):
    """Product schema for API."""

    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0, description="Price per unit")
    quantity: int = Field(ge=0, description="Current stock quantity")
    reorder_level: int = Field(default=10, description="Low stock threshold")
    supplier: Optional[str] = None
    category: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CustomerSchema(BaseModel):
    """Customer schema for API."""

    id: Optional[str] = None
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    total_purchases: float = Field(default=0.0)
    purchase_count: int = Field(default=0)
    last_purchase_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class StaffSchema(BaseModel):
    """Staff member schema for API."""

    id: Optional[str] = None
    name: str
    role: str  # manager, cashier, inventory, etc.
    email: Optional[str] = None
    phone: Optional[str] = None
    hire_date: Optional[datetime] = None
    status: str = Field(default="active")  # active, inactive, on_leave
    performance_rating: float = Field(default=0.0, ge=0.0, le=5.0)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TransactionItemSchema(BaseModel):
    """Item in a transaction."""

    product_id: str
    product_name: str
    quantity: int
    unit_price: float
    total: float


class TransactionSchema(BaseModel):
    """Transaction/Order schema for API."""

    id: Optional[str] = None
    customer_id: Optional[str] = None
    customer_name: Optional[str] = None
    items: List[TransactionItemSchema]
    subtotal: float
    tax: float = Field(default=0.0, ge=0.0)
    total: float
    payment_method: str = Field(default="cash")  # cash, card, transfer
    notes: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BusinessStateSchema(BaseModel):
    """Current business state snapshot."""

    total_cash: float = Field(default=0.0)
    total_inventory_value: float = Field(default=0.0)
    daily_sales: float = Field(default=0.0)
    daily_transactions: int = Field(default=0)
    total_products: int = Field(default=0)
    low_stock_count: int = Field(default=0)
    total_customers: int = Field(default=0)
    total_staff: int = Field(default=0)
    last_updated: datetime
    period: str = Field(default="today")  # today, week, month


class TaskSchema(BaseModel):
    """Task schema for agent execution."""

    id: Optional[str] = None
    description: str
    agents: List[str] = Field(default_factory=list)
    priority: str = Field(default="normal")  # low, normal, high, critical
    status: str = Field(default="pending")  # pending, running, completed, failed
    result: Optional[dict] = None
    error: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# SQLALCHEMY ORM MODELS
# ============================================================================


class Product(Base):
    """Product database model."""

    __tablename__ = "products"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    reorder_level = Column(Integer, nullable=False, default=10)
    supplier = Column(String(255), nullable=True)
    category = Column(String(100), nullable=True, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class Customer(Base):
    """Customer database model."""

    __tablename__ = "customers"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), nullable=True, unique=True)
    phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    total_purchases = Column(Float, nullable=False, default=0.0)
    purchase_count = Column(Integer, nullable=False, default=0)
    last_purchase_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class Staff(Base):
    """Staff member database model."""

    __tablename__ = "staff"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    role = Column(String(100), nullable=False)
    email = Column(String(255), nullable=True, unique=True)
    phone = Column(String(20), nullable=True)
    hire_date = Column(DateTime, nullable=True)
    status = Column(String(50), nullable=False, default="active")
    performance_rating = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class Transaction(Base):
    """Transaction/Order database model."""

    __tablename__ = "transactions"

    id = Column(String(36), primary_key=True, index=True)
    customer_id = Column(String(36), nullable=True, index=True)
    customer_name = Column(String(255), nullable=True)
    items = Column(JSON, nullable=False)  # List of items with product_id, qty, price
    subtotal = Column(Float, nullable=False)
    tax = Column(Float, nullable=False, default=0.0)
    total = Column(Float, nullable=False)
    payment_method = Column(String(50), nullable=False, default="cash")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)


class BusinessMetrics(Base):
    """Business metrics tracking."""

    __tablename__ = "business_metrics"

    id = Column(String(36), primary_key=True, index=True)
    total_cash = Column(Float, nullable=False, default=0.0)
    total_inventory_value = Column(Float, nullable=False, default=0.0)
    daily_sales = Column(Float, nullable=False, default=0.0)
    daily_transactions = Column(Integer, nullable=False, default=0)
    period = Column(String(50), nullable=False, default="today")
    recorded_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)


class Task(Base):
    """Task/Job database model."""

    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True, index=True)
    description = Column(Text, nullable=False)
    agents = Column(JSON, nullable=False, default=[])
    priority = Column(String(50), nullable=False, default="normal")
    status = Column(String(50), nullable=False, default="pending", index=True)
    result = Column(JSON, nullable=True)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
