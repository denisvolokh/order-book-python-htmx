import random
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
import asyncio
from sse_starlette import ServerSentEvent
from sse_starlette.sse import EventSourceResponse



app = FastAPI()
templates = Jinja2Templates(directory="templates")


def generate_bid_ask_data():
    """Generates and returns sorted bid and ask data, along with current price and max quantities.
    """    

    # Bids: Higher price -> Lower quantity
    bids = [
        {"price": round(random.uniform(100 + i * 0.5, 105), 2), "quantity": random.randint(10, 100 - i * 9)}
        for i in range(10)
    ]

    # Asks: Lower price -> Lower quantity
    asks = [
        {"price": round(random.uniform(105 + i * 0.5, 110), 2), "quantity": random.randint(10 + i * 9, 100)}
        for i in range(10)
    ]

    bids = sorted(bids, key=lambda x: x["price"], reverse=True)
    asks = sorted(asks, key=lambda x: x["price"], reverse=True)

    current_price = round((bids[0]["price"] + asks[0]["price"]) / 2, 2)

    # Calculate maximum quantities for both bids and asks
    max_bid_quantity = max(bid["quantity"] for bid in bids) if bids else 1
    max_ask_quantity = max(ask["quantity"] for ask in asks) if asks else 1

    return {
        "bids": bids,
        "asks": asks,
        "current_price": current_price,
        "max_bid_quantity": max_bid_quantity,
        "max_ask_quantity": max_ask_quantity,
    }


@app.get("/orderbook")
async def orderbook_page(request: Request):
    return templates.TemplateResponse("orderbook.html", {"request": request})


@app.get("/orderbook/update", response_class=HTMLResponse)
async def update_table(request: Request):
    data = generate_bid_ask_data()

    return templates.TemplateResponse(
        "orderbook_data.html",
        {
            "request": request,
            **data
        }
    )


async def event_generator():
    template = templates.get_template("orderbook_data.html")
    while True:
        data = generate_bid_ask_data()

        rendered_data = template.render(
            bids=data["bids"],
            asks=data["asks"],
            current_price=data["current_price"],
            max_bid_quantity=data["max_bid_quantity"],
            max_ask_quantity=data["max_ask_quantity"]
        )

        yield ServerSentEvent(rendered_data)

        await asyncio.sleep(1)


@app.get("/orderbook/stream")
async def orderbook_stream(request: Request):
    return EventSourceResponse(event_generator())