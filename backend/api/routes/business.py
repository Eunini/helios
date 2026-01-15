"""Business data endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from core import get_db, logger
from memory import (
    ProductSchema,
    CustomerSchema,
    StaffSchema,
    TransactionSchema,
    BusinessStateSchema,
)
from services import (
    InventoryService,
    CustomerService,
    StaffService,
    OrderService,
    ReportService,
)
from memory.state_store import StateStore

router = APIRouter()


# ============================================================================
# PRODUCTS / INVENTORY
# ============================================================================

@router.post("/products", response_model=ProductSchema)
async def create_product(
    product: ProductSchema,
    db: Session = Depends(get_db),
):
    """Create a new product."""
    try:
        service = InventoryService(db)
        db_product = service.create_product(product)
        return db_product
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/products/{product_id}", response_model=ProductSchema)
async def get_product(
    product_id: str,
    db: Session = Depends(get_db),
):
    """Get product by ID."""
    service = InventoryService(db)
    product = service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/products", response_model=List[ProductSchema])
async def list_products(
    category: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """List all products."""
    service = InventoryService(db)
    return service.get_all_products(category)


@router.put("/products/{product_id}", response_model=ProductSchema)
async def update_product(
    product_id: str,
    product: ProductSchema,
    db: Session = Depends(get_db),
):
    """Update product."""
    try:
        service = InventoryService(db)
        updated = service.update_product(product_id, product)
        if not updated:
            raise HTTPException(status_code=404, detail="Product not found")
        return updated
    except Exception as e:
        logger.error(f"Error updating product: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/products/{product_id}/add-stock")
async def add_stock(
    product_id: str,
    quantity: int = Query(gt=0),
    db: Session = Depends(get_db),
):
    """Add stock to product."""
    try:
        service = InventoryService(db)
        updated = service.add_stock(product_id, quantity)
        if not updated:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"status": "success", "product": updated}
    except Exception as e:
        logger.error(f"Error adding stock: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/products/{product_id}/remove-stock")
async def remove_stock(
    product_id: str,
    quantity: int = Query(gt=0),
    db: Session = Depends(get_db),
):
    """Remove stock from product."""
    try:
        service = InventoryService(db)
        updated = service.remove_stock(product_id, quantity)
        if not updated:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"status": "success", "product": updated}
    except Exception as e:
        logger.error(f"Error removing stock: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/products/low-stock")
async def get_low_stock(
    db: Session = Depends(get_db),
):
    """Get low stock products."""
    service = InventoryService(db)
    return service.get_low_stock_products()


@router.delete("/products/{product_id}")
async def delete_product(
    product_id: str,
    db: Session = Depends(get_db),
):
    """Delete product."""
    try:
        service = InventoryService(db)
        success = service.delete_product(product_id)
        if not success:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"status": "deleted"}
    except Exception as e:
        logger.error(f"Error deleting product: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# CUSTOMERS
# ============================================================================

@router.post("/customers", response_model=CustomerSchema)
async def create_customer(
    customer: CustomerSchema,
    db: Session = Depends(get_db),
):
    """Create a new customer."""
    try:
        service = CustomerService(db)
        return service.create_customer(customer)
    except Exception as e:
        logger.error(f"Error creating customer: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/customers/{customer_id}", response_model=CustomerSchema)
async def get_customer(
    customer_id: str,
    db: Session = Depends(get_db),
):
    """Get customer by ID."""
    service = CustomerService(db)
    customer = service.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.get("/customers", response_model=List[CustomerSchema])
async def list_customers(
    db: Session = Depends(get_db),
):
    """List all customers."""
    service = CustomerService(db)
    return service.get_all_customers()


@router.put("/customers/{customer_id}", response_model=CustomerSchema)
async def update_customer(
    customer_id: str,
    customer: CustomerSchema,
    db: Session = Depends(get_db),
):
    """Update customer."""
    try:
        service = CustomerService(db)
        updated = service.update_customer(customer_id, customer)
        if not updated:
            raise HTTPException(status_code=404, detail="Customer not found")
        return updated
    except Exception as e:
        logger.error(f"Error updating customer: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/customers/{customer_id}")
async def delete_customer(
    customer_id: str,
    db: Session = Depends(get_db),
):
    """Delete customer."""
    try:
        service = CustomerService(db)
        success = service.delete_customer(customer_id)
        if not success:
            raise HTTPException(status_code=404, detail="Customer not found")
        return {"status": "deleted"}
    except Exception as e:
        logger.error(f"Error deleting customer: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# STAFF
# ============================================================================

@router.post("/staff", response_model=StaffSchema)
async def create_staff(
    staff: StaffSchema,
    db: Session = Depends(get_db),
):
    """Create a new staff member."""
    try:
        service = StaffService(db)
        return service.create_staff(staff)
    except Exception as e:
        logger.error(f"Error creating staff: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/staff/{staff_id}", response_model=StaffSchema)
async def get_staff(
    staff_id: str,
    db: Session = Depends(get_db),
):
    """Get staff member by ID."""
    service = StaffService(db)
    staff = service.get_staff(staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    return staff


@router.get("/staff", response_model=List[StaffSchema])
async def list_staff(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """List staff members."""
    service = StaffService(db)
    return service.get_all_staff(status)


@router.put("/staff/{staff_id}", response_model=StaffSchema)
async def update_staff(
    staff_id: str,
    staff: StaffSchema,
    db: Session = Depends(get_db),
):
    """Update staff member."""
    try:
        service = StaffService(db)
        updated = service.update_staff(staff_id, staff)
        if not updated:
            raise HTTPException(status_code=404, detail="Staff not found")
        return updated
    except Exception as e:
        logger.error(f"Error updating staff: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/staff/{staff_id}")
async def delete_staff(
    staff_id: str,
    db: Session = Depends(get_db),
):
    """Delete staff member."""
    try:
        service = StaffService(db)
        success = service.delete_staff(staff_id)
        if not success:
            raise HTTPException(status_code=404, detail="Staff not found")
        return {"status": "deleted"}
    except Exception as e:
        logger.error(f"Error deleting staff: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# TRANSACTIONS
# ============================================================================

@router.post("/transactions", response_model=TransactionSchema)
async def create_transaction(
    transaction: TransactionSchema,
    db: Session = Depends(get_db),
):
    """Create a new transaction."""
    try:
        service = OrderService(db)
        return service.create_transaction(transaction)
    except Exception as e:
        logger.error(f"Error creating transaction: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/transactions/{transaction_id}", response_model=TransactionSchema)
async def get_transaction(
    transaction_id: str,
    db: Session = Depends(get_db),
):
    """Get transaction by ID."""
    service = OrderService(db)
    transaction = service.get_transaction(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.get("/transactions", response_model=List[TransactionSchema])
async def list_transactions(
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db),
):
    """List transactions."""
    service = OrderService(db)
    return service.get_all_transactions(limit)


# ============================================================================
# BUSINESS STATE
# ============================================================================

@router.get("/state", response_model=BusinessStateSchema)
async def get_business_state(
    db: Session = Depends(get_db),
):
    """Get current business state."""
    try:
        state_store = StateStore(db)
        
        inventory_service = InventoryService(db)
        products = inventory_service.get_all_products()
        total_inventory_value = sum(p.price * p.quantity for p in products)
        
        order_service = OrderService(db)
        daily_sales = order_service.calculate_daily_sales()
        transactions = order_service.get_all_transactions(limit=None)
        
        customer_service = CustomerService(db)
        customers = customer_service.get_all_customers()
        
        staff_service = StaffService(db)
        staff_members = staff_service.get_all_staff()
        
        low_stock = inventory_service.get_low_stock_products()
        
        return BusinessStateSchema(
            total_cash=sum(t.total for t in transactions) if transactions else 0.0,
            total_inventory_value=total_inventory_value,
            daily_sales=daily_sales,
            daily_transactions=len(transactions),
            total_products=len(products),
            low_stock_count=len(low_stock),
            total_customers=len(customers),
            total_staff=len(staff_members),
            last_updated=datetime.utcnow(),
            period="today",
        )
    except Exception as e:
        logger.error(f"Error getting business state: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# REPORTS
# ============================================================================

@router.get("/reports/comprehensive")
async def get_comprehensive_report(
    db: Session = Depends(get_db),
):
    """Get comprehensive business report."""
    try:
        service = ReportService(db)
        return service.get_comprehensive_report()
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reports/daily")
async def get_daily_report(
    db: Session = Depends(get_db),
):
    """Get daily business summary."""
    try:
        service = ReportService(db)
        return service.get_daily_summary()
    except Exception as e:
        logger.error(f"Error generating daily report: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reports/inventory")
async def get_inventory_report(
    db: Session = Depends(get_db),
):
    """Get inventory report."""
    try:
        service = ReportService(db)
        return service.get_inventory_report()
    except Exception as e:
        logger.error(f"Error generating inventory report: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reports/customers")
async def get_customer_report(
    db: Session = Depends(get_db),
):
    """Get customer report."""
    try:
        service = ReportService(db)
        return service.get_customer_report()
    except Exception as e:
        logger.error(f"Error generating customer report: {e}")
        raise HTTPException(status_code=500, detail=str(e))
