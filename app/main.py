from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
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

@app.get("/")
def read_root():
    # test database
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT 'database working' as msg, version() AS version
        """)
        db_status = cur.fetchone();
    return { "msg": "Welcome to the hotel booking-API", "db": db_status}

@app.get("/rooms")
def get_rooms():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT room_number, type AS room_type, price AS room_price
            FROM hotel_rooms 
            ORDER BY room_number
        """)
        return cur.fetchall()