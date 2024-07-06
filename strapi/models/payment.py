from sqlmodel import SQLModel, Field, String
from typing import Optional

# Note: This All For Testing Purpose to test payment api key rather its running or not so please defined your own models and modifie at your self

class Payment(SQLModel, table=True):
    payment_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int # match your user_id using foregin key for your user_service
    user_email: str  # Define User Email That Link to your user_service example: userexample@gmail.com
    request_id: int # genrate your random request_id what ever you want to genrate
    amount: int     # example your amount
    currency: str   # define your currency but note: that the currency only accesseptable for world wide only pkr not accessiptable
    order_id: str   # define your order id that links to your order_service with foregin key

class CheckoutRequest(SQLModel):
    user_id: int
    user_email: str
    request_id: int
    price: int
    product_name: str
    quantity: int
    
# Use this when you need to integrated order api with payment dynamically for now im doing simple as a testing purpose only when the order created then user will create payment.  

# class Order(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     user_id: int
#     product_name: str
#     quantity: int
#     total_price: int