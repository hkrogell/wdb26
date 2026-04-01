from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rooms = [
    { "room_number": 1, "room_type": "Suite", "room_price": 1000},
    { "room_number": 2, "room_type": "Double Bed", "room_price": 500},
    { "room_number": 3, "room_type": "Presidential", "room_price": 10000},
]

@app.get("/")
def read_root():
    return { "msg": "Welcome to the hotel booking-API" }

@app.get("/rooms")
def get_rooms():
    return rooms