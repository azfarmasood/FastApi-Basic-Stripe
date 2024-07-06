from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from strapi.database.db import get_tables, DB_SESSION, strip_secret_key
from sqlmodel import select
from strapi.models.payment import Payment, CheckoutRequest
from strapi.strip_config.strip_config import create_checkout
import stripe

app = FastAPI(lifespan = get_tables)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


stripe.api_key = strip_secret_key

@app.get("/payment-status/{user_id}")
async def get_payment_status(user_id: int, db: DB_SESSION):
    try:
        statement = select(Payment).where(Payment.user_id == user_id)
        results = db.exec(statement)
        payments = results.all()
        if not payments:
            return {"message": "No payments found for this user."}
            
        payment_statuses = []
        for payment in payments:
            session_data = stripe.checkout.Session.retrieve(payment.order_id)
            status = session_data.payment_status
            if status == "paid":
                payment_statuses.append({"order_id": payment.order_id, "status": "Payment successful"})
            else:
                payment_statuses.append({"order_id": payment.order_id, "status": "Payment pending"})

        return {"payments": payment_statuses}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@app.post("/check-out/")
async def create_checkouts(check_out_request: CheckoutRequest, db: DB_SESSION):
    return await create_checkout(check_out_request = check_out_request, db = db)