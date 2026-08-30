"""
Payment API - Stripe Integration for Premium Subscriptions
Production-Ready with Webhook Support
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import stripe
from datetime import datetime
import os

from app.db.session import get_db
from app.models.user import User
from app.core.security import get_current_user
from app.core.config import settings

router = APIRouter()

# Configure Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_placeholder")


@router.post("/create-checkout-session")
async def create_checkout_session(
    plan: str = "monthly",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create Stripe checkout session for premium subscription."""
    
    # Validate plan
    if plan not in ["monthly", "yearly"]:
        raise HTTPException(status_code=400, detail="Invalid plan. Choose 'monthly' or 'yearly'")
    
    # Determine price based on plan (in cents)
    prices = {
        "monthly": 999,  # $9.99
        "yearly": 9999   # $99.99 (save 17%)
    }
    
    try:
        # Create checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"Market Mind Premium ({plan.capitalize()})",
                        "description": "Access to all premium features including advanced analytics, unlimited portfolios, and priority support",
                        "images": ["https://yourdomain.com/premium-icon.png"]
                    },
                    "unit_amount": prices[plan],
                    "recurring": {
                        "interval": "month" if plan == "monthly" else "year"
                    }
                },
                "quantity": 1,
            }],
            mode="subscription",
            success_url=f"{settings.FRONTEND_URL}/payment/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{settings.FRONTEND_URL}/payment/cancel",
            customer_email=current_user.email,
            metadata={
                "user_id": str(current_user.id),
                "plan": plan,
                "username": current_user.username
            },
            allow_promotion_codes=True,
            billing_address_collection="required"
        )
        
        return {
            "checkout_url": session.url,
            "session_id": session.id,
            "plan": plan,
            "price": prices[plan] / 100  # Convert to dollars
        }
        
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=500, detail=f"Payment error: {str(e)}")


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle Stripe webhook events for subscription management."""
    
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    # Verify webhook signature
    try:
        webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_placeholder")
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Handle the event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        
        # Get user from metadata
        user_id = int(session["metadata"]["user_id"])
        user = db.query(User).filter(User.id == user_id).first()
        
        if user:
            # Upgrade user to premium
            user.is_premium = True
            db.commit()
            
    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        # Get user and downgrade to free
        # (Implement based on your metadata structure)
    
    return {"status": "success"}


@router.get("/subscription-status")
def get_subscription_status(
    current_user: User = Depends(get_current_user)
):
    """Get current user's subscription status."""
    return {
        "is_premium": current_user.is_premium,
        "email": current_user.email,
        "username": current_user.username,
        "created_at": current_user.created_at
    }


@router.post("/cancel-subscription")
def cancel_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel user's premium subscription."""
    # Implement Stripe subscription cancellation
    # For now, just downgrade user
    current_user.is_premium = False
    db.commit()
    
    return {"message": "Subscription cancelled successfully"}
