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
        for _ in range(5)
    ]
    asks = [
        {"price": round(random.uniform(106, 110), 2), "quantity": random.randint(1, 50)}
        for _ in range(5)
    ]

    # Sort bids in ascending order (lowest prices first)
    bids = sorted(bids, key=lambda x: x["price"], reverse=True)

    # Sort asks in descending order (highest prices first)
    asks = sorted(asks, key=lambda x: x["price"], reverse=True)

    order_book = {"bids": bids, "asks": asks}

    # Pass the "request" and sorted order_book to the template
    return templates.TemplateResponse("orderbook_data.html", {"request": request, "order_book": order_book})