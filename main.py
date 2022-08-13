from ast import Add
from cv2 import add
from fastapi import Depends, FastAPI,HTTPException
from requests import session
from sqlalchemy import Float
import models
from database import engine, sessionlocal
from sqlalchemy.orm import Session
from pydantic import BaseModel,Field

app = FastAPI() #Initializing FastAPI

models.Base.metadata.create_all(bind=engine)

#Connecting to Db with the help of sessionlocal package
def get_db():
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()

#Initializing Class attributes for address
class Address(BaseModel):
    lat: float
    long: float
    location: str

#Retrieving all the records available in the DB
@app.get("/")
async def read_all_address(db:Session = Depends(get_db)):#Adding Depends keyword for Db to start up before executing the query
    return db.query(models.Address).all()


#Retrieving the values based on address_id
@app.get("/address/{address_id}")
async def get_address_by_id(id:int, db:Session = Depends(get_db)):
    address_model = db.query(models.Address).filter(models.Address.id == id).first()
    if address_model is not None:
        return address_model
    raise http_exception()

#Adding the records to the Database
@app.post("/")
async def create_address(address:Address, db:Session = Depends(get_db)):
    address_model = models.Address()
    address_model.lat = address.lat
    address_model.long = address.long
    address_model.location = address.location

    db.add(address_model)
    db.commit()

    return successfull_response(200)

#Updating the records based on id provided
@app.put("/{id}")
async def update_address(id:int, address:Address, db:Session = Depends(get_db)):
    address_model = db.query(models.Address).filter(models.Address.id == id).first()

    if address_model is None:
        raise http_exception()

    address_model.lat = address.lat
    address_model.long = address.long
    address_model.location = address.location

    db.add(address_model)
    db.commit()

    return successfull_response(200)

#Deleting the entry from DB for the ID given
@app.delete("/{id}")
async def delete_address(id:int, db: Session = Depends(get_db)):
    address_model = db.query(models.Address).filter(models.Address.id == id).first()

    if address_model is None:
        raise http_exception()

    db.query(models.Address).filter(models.Address.id == id).delete()

    db.commit()

    return successfull_response(200)


#Retrieve the location based on lattitude and Longitude Provided
@app.get("/{lat_lon}")
async def get_address_by_distance(lat:float,long:float, db: Session = Depends(get_db)):
    lat_value = db.query(models.Address).filter(models.Address.lat == lat).first()
    long_value = db.query(models.Address).filter(models.Address.long == long).first()

    if lat_value and long_value is not None:
        return db.query(models.Address.location).filter(models.Address.lat == lat,models.Address.long == long).first()

    raise http_exception()

#Comman Success Function
def successfull_response(status_code:int):
    return {
        'status':status_code,
        'transaction':"Successfull"
    }
#Common Exception Handler
def http_exception():
    return HTTPException(status_code=404,detail="Address Id not found")
