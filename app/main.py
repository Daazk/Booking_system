from fastapi import FastAPI
from app.routers import rooms, bookings

app = FastAPI(title="Booking system")


app.include_router(rooms.router)
app.include_router(bookings.router)
