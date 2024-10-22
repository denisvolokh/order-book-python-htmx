import random
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/orderbook")
async def orderbook_page(request: Request):
    return templates.TemplateResponse("orderbook.html", {"request": request})


@app.get("/orderbook/update", response_class=HTMLResponse)
async def orderbook_update(request: Request):
    # Generate random order book data
    bids = [
        {"price": round(random.uniform(100, 105), 2), "quantity": random.randint(1, 50)}
        for _ in range(10)
    ]
    asks = [
        {"price": round(random.uniform(106, 110), 2), "quantity": random.randint(1, 50)}
        for _ in range(10)
    ]

    bids = sorted(bids, key=lambda x: x["price"], reverse=True)
    asks = sorted(asks, key=lambda x: x["price"], reverse=True)

    # Calculate current price (midpoint between highest bid and lowest ask)
    highest_bid = bids[-1]["price"] if bids else None
    lowest_ask = asks[-1]["price"] if asks else None
    current_price = None
    if highest_bid and lowest_ask:
        current_price = round((highest_bid + lowest_ask) / 2, 2)

    order_book = {"bids": bids, "asks": asks, "current_price": current_price}

    return templates.TemplateResponse(
        "orderbook_data.html", {"request": request, "order_book": order_book}
    )
