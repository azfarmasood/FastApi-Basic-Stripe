from fastapi import HTTPException, responses
from strapi.database.db import base_url, DB_SESSION
from strapi.models.payment import CheckoutRequest, Payment
import stripe

async def create_checkout(check_out_request: CheckoutRequest, db: DB_SESSION):
    try:
        total_price = check_out_request.price * check_out_request.quantity
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": check_out_request.product_name,
                        },
                        "unit_amount": check_out_request.price * 100,
                    },
                    "quantity": check_out_request.quantity,
                }
            ],
            metadata={
                "user_id": check_out_request.user_id,
                "email": check_out_request.user_email,
                "request_id": check_out_request.request_id
            },
            mode="payment",
            success_url=f"{base_url}/success/",
            cancel_url=f"{base_url}/cancel/",
            customer_email=check_out_request.user_email,
        )
        if not checkout_session.url:
            raise HTTPException(status_code=400, detail="Failed to create checkout session URL")
        
        new_payment = Payment(
            user_id=check_out_request.user_id,
            user_email=check_out_request.user_email,
            request_id=check_out_request.request_id,
            amount=total_price,
            currency="usd",
            order_id=checkout_session.id,
        )
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)
        
        return {
            "message": "Payment created successfully",
            "checkout_url": checkout_session.url
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
