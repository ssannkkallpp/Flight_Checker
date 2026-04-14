from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import psycopg2
import psycopg2.extras
from datetime import datetime, date
from dotenv import load_dotenv
import os


app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db_connection():
    conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    )
    return conn

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/flights", response_class=HTMLResponse)
def all_flights(request: Request, origin_code: str = Form(...), dest_code: str = Form(...), start_date: str = Form(...), end_date: str = Form(...)):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("select fs.flight_number, fs.airline_name, fs.origin_code, fs.dest_code, f.departure_date, fs.departure_time from flightservice fs join flight f on fs.flight_number = f.flight_number where fs.origin_code = %s and fs.dest_code = %s and f.departure_date BETWEEN %s AND %s order by f.departure_date, fs.departure_time", (origin_code, dest_code, start_date, end_date))
    flights = cur.fetchall()
    cur.close()
    conn.close()
    return templates.TemplateResponse(request=request, name="flights.html", context={"flights": flights, "origin": origin_code,
    "dest": dest_code,
    "start_date": start_date,
    "end_date": end_date})


@app.get("/seats/{flight_number}/{departure_date}", response_class=HTMLResponse)
def flight_booking(request: Request, flight_number: str, departure_date: str):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    parsed_date = date.fromisoformat(departure_date)
    cur.execute("select f.flight_number, f.departure_date, ac.capacity, count(b.pid) as booked_seats, ac.capacity - count(b.pid) as available_seats from flight f join aircraft ac on f.plane_type = ac.plane_type left join booking b on f.flight_number = b.flight_number and f.departure_date = b.departure_date where f.flight_number = %s and f.departure_date = %s group by f.flight_number, f.departure_date, ac.capacity", (flight_number, parsed_date))
    seats = cur.fetchone()
    cur.close()
    conn.close()
    return templates.TemplateResponse(request=request, name="flight_details.html", context={"detail": seats})
