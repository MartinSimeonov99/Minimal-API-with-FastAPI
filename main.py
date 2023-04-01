from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from math import sin, cos, sqrt, atan2, radians
import sqlite3

import uvicorn

app = FastAPI()

# Define the data model for addresses
class Address(BaseModel):
    address: str
    latitude: float
    longitude: float

# Define a function to calculate the distance between two coordinates
def distance(lat1, lon1, lat2, lon2):
    R = 6373.0 # approximate radius of Earth in km

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance_km = R * c
    return distance_km

# Define the endpoints for creating, updating, and deleting addresses
@app.post("/address")
def create_address(address: Address):
    conn = sqlite3.connect('addresses.db')
    c = conn.cursor()
    c.execute('INSERT INTO addresses (address, latitude, longitude) VALUES (?, ?, ?)',
              (address.address, address.latitude, address.longitude))
    conn.commit()
    conn.close()
    return {"message": "Address created"}

@app.put("/address/{id}")
def update_address(id: int, address: Address):
    conn = sqlite3.connect('addresses.db')
    c = conn.cursor()
    c.execute('UPDATE addresses SET address=?, latitude=?, longitude=? WHERE id=?',
              (address.address, address.latitude, address.longitude, id))
    conn.commit()
    conn.close()
    return {"message": "Address updated"}

@app.delete("/address/{id}")
def delete_address(id: int):
    conn = sqlite3.connect('addresses.db')
    c = conn.cursor()
    c.execute('SELECT * FROM addresses WHERE id=?', (id,))
    address = c.fetchone()
    if address is None:
        return {"message": "Address not found"}
    c.execute('DELETE FROM addresses WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return {"message": "Address deleted"}


# Define the endpoint for retrieving addresses within a certain distance and location
@app.get("/addresses")
def get_addresses(latitude: float, longitude: float, radius: int):
    conn = sqlite3.connect('addresses.db')
    c = conn.cursor()
    c.execute('SELECT id, address, latitude, longitude FROM addresses')
    rows = c.fetchall()

    addresses_within_radius = []
    for row in rows:
        dist = distance(latitude, longitude, row[2], row[3])
        if dist <= radius:
            addresses_within_radius.append({"id": row[0], "address": row[1], "latitude": row[2], "longitude": row[3], "distance_km": dist})
    
    conn.close()
    return {"addresses": addresses_within_radius}

if __name__ == "__main__":
    # Create the SQLite database table if it doesn't exist
    conn = sqlite3.connect('addresses.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS addresses (id INTEGER PRIMARY KEY, address TEXT, latitude REAL, longitude REAL)')
    conn.commit()
    conn.close()

    # Start the Uvicorn web server
    uvicorn.run("main:app", host="192.168.1.104", port=8000, reload=True)
