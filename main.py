from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from order_routes import order_router
from pizza_routes import pizza_router
from database import init_db


app=FastAPI()


app.include_router(order_router)
app.include_router(pizza_router)


origins=[
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Content-Type", "*"],
)
@app.on_event("startup")
async def startup_event():
    await init_db()