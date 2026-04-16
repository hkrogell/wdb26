from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date
from app.db import get_conn, create_schema

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# create database schema
create_schema()

class Booking(BaseModel):
    guest_id: int
    room_id: int
    datefrom: date
    dateto: date

# main route for hotel API
@app.get("/")
def read_root():
    # test database
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT 'database working' as msg, version() AS version
        """)
        db_status = cur.fetchone()
    return { "msg": "Welcome to the hotel booking-API", "db": db_status}

# get all rooms
@app.get("/rooms")
def get_rooms():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT *
            FROM rooms 
            ORDER BY room_number
        """)
        rooms = cur.fetchall()
    return rooms
    
# get one room by id
@app.get("/rooms/{id}")
def get_room(id: int):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT *
            FROM rooms 
            WHERE id = %s
        """, [id])
        room = cur.fetchone()
    return room

# list all bookings
@app.get("/bookings")
def get_bookings():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT *
            FROM bookings
            ORDER BY id
        """)
        bookings = cur.fetchall()
    return bookings

# create a booking
@app.post("/bookings")
def create_booking(booking: Booking):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            INSERT INTO bookings (
                guest_id,
                room_id,
                datefrom,
                dateto
            ) VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (booking.guest_id, 
              booking.room_id, 
              booking.datefrom, 
              booking.dateto))
        booking_id = cur.fetchone()["id"]
    return { "msg": "Booking created", "id": booking_id }
