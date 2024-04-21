from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from order_routes import order_router
from pizza_routes import pizza_router
from database import init_db
from demo_auth.views import router as auth_router
from category_routes import category_router as cat_router
from fastapi.staticfiles import StaticFiles


app=FastAPI()
app.mount('/static', StaticFiles(directory='static'),name='static')

app.include_router(order_router)
app.include_router(pizza_router)
app.include_router(auth_router)
app.include_router(cat_router)


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