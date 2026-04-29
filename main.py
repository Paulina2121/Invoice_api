from fastapi import FastAPI, HTTPException, Query, Header, Depends
from pydantic import BaseModel
from datetime import date as Date
from dotenv import load_dotenv
import os
import database  # CSV or database in SQL

app = FastAPI(title="Invoice DB")

load_dotenv(override=True)
API_KEY = os.getenv("API_KEY")

# --- SCHEMA ---
class InvoiceBase(BaseModel):
    invoice_number: str
    date: Date
    due_date: Date
    order_number: str
    vat_percent: float | None = None

class InvoiceCreate(InvoiceBase):
    pass

class Invoice(InvoiceBase):
    id: int


class InvoiceUpdate(BaseModel):
    date: Date | None = None
    due_date: Date | None = None
    order_number: str | None = None
    vat_percent: float | None = None


def check_api_key(x_secret: str = Header(...)):
    if x_secret==API_KEY:
        return
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


# --- ENDPOINTS ---
@app.get("/invoices", response_model=list[Invoice], status_code=200,tags=["invoice"],dependencies=[Depends(check_api_key)])
def get_invoices(limit: int| None = Query(default=None, ge=1)):
    return database.get_all_invoices(limit)


@app.get("/invoice/{invoice_id}", response_model=list[Invoice],tags=["invoice"],dependencies=[Depends(check_api_key)])
def get_invoices(invoice_id: int):
    result =  database.get_invoice_details(invoice_id)

    if result == "not found":
        raise HTTPException(status_code=404, detail=f"API Error: invoice_id not found")
    else:
        return result


@app.post("/invoice/create", status_code=201,tags=["invoice"],dependencies=[Depends(check_api_key)])
def create_invoice(invoice_data: InvoiceCreate):
    try:
        database.add_invoice(invoice_data)
        return "Invoice added"
    except ValueError as e:
        raise HTTPException(status_code=409, detail=f"API Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"API Error: {str(e)}")


@app.patch("/invoice/update/{invoice_id}", status_code=200,tags=["invoice"],dependencies=[Depends(check_api_key)])
def update_invoice(invoice_id: int, invoice_data: InvoiceUpdate):
    try:
        database.update_invoice(invoice_id, invoice_data)
        return "The update was successful."
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"API Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"API Error: {str(e)}")
    

@app.delete("/invoice/{invoice_id}", status_code=204,tags=["invoice"],dependencies=[Depends(check_api_key)])
def delete_invoice(invoice_id: int):
    
    try:
        database.delete_invoice(invoice_id)
        return "Invoice deleted"
    except ValueError as e:
        raise HTTPException(status_code=409, detail=f"API Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"API Error: {str(e)}") 
