#Medical Appointment System
from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import List, Optional
import math

app=FastAPI()

class AppointmentRequest(BaseModel):
    patient_name: str = Field(..., min_length=2)
    doctor_id: int = Field(..., gt=0)
    date: str = Field(..., min_length=8)
    reason: str = Field(..., min_length=5)
    appointment_type: str = "in-person"
    senior_citizen: bool = False

class NewDoctor(BaseModel):
    name: str = Field(..., min_length=2)
    specialization: str = Field(..., min_length=2)
    fee: int = Field(..., gt=0)
    experience_years: int = Field(..., gt=0)
    is_available: bool = True


#Data Entry
doctors=[
    {"id": 1, "name": "Dr. Mohith", "specialization": "Cardiologist", "fee": 700, "experience_years": 9, "is_available": True},
    {"id": 2, "name": "Dr. John", "specialization": "Dermatologist", "fee": 600, "experience_years": 7, "is_available": True},
    {"id": 3, "name": "Dr. Rutvik", "specialization": "Dentist", "fee": 400, "experience_years": 8, "is_available": False},
    {"id": 4, "name": "Dr. Fardin", "specialization": "General", "fee": 200, "experience_years": 5, "is_available": True},
    {"id": 5, "name": "Dr. Abhi", "specialization": "Cardiologist", "fee": 600, "experience_years": 12, "is_available": True},
    {"id": 6, "name": "Dr. David", "specialization": "Dermatologist", "fee": 350, "experience_years": 6, "is_available": False},
]

#Helper Functions
def find_doctor(doctor_id):
    for doctor in doctors:
        if doctor['id']==doctor_id:
            return doctor
    return None

def calculate_fee(base_fee, appointment_type, senior_citizen):
    if appointment_type=="video":
        fee=base_fee*0.8
    elif appointment_type=="emergency":
        fee=base_fee*1.5
    else:
        fee=base_fee
    if senior_citizen:
        final_fee=fee*0.85
    else:
        final_fee=fee
    return {"original_fee":base_fee, "final_fee":int(final_fee)}

def filter_doctors_logic(specialization, max_fee, min_exp, is_available):
    result = doctors
    if specialization is not None:
        result = [d for d in result if d["specialization"].lower() == specialization.lower()]
    if max_fee is not None:
        result = [d for d in result if d["fee"] <= max_fee]
    if min_exp is not None:
        result = [d for d in result if d["experience_years"] >= min_exp]
    if is_available is not None:
        result = [d for d in result if d["is_available"] == is_available]

    return result

def find_appointment(appt_id):
    for a in appointments:
        if a["appointment_id"] == appt_id:
            return a
    return None

#1Endpoint 1:
@app.get('/')
def get_root():
    return {'message': 'Welcome to MediCare Clinic'}

#Endpoint 2:
@app.get('/doctors')
def get_doctors():
    doctors_available=[doctor for doctor in doctors if doctor['is_available']==True]
    return {'total':len(doctors), 'available_count':len(doctors_available), 'doctors':doctors}


#Endpoint 5:
@app.get('/doctors/summary')
def get_doctors_summary():
    if not doctors:
        return {'message': 'No doctors found'}
    high_experienced=max(doctors, key=lambda x: x['experience_years'])
    cheapest=min(doctors, key=lambda x: x['fee'])
    specialisation={}
    for doctor in doctors:
        specialisation[doctor['specialization']]=specialisation.get(doctor['specialization'], 0)+1
    return {'total':len(doctors),'available':len([d for d in doctors if d["is_available"]]), 'most_experienced':high_experienced["name"], 'cheapest_fee':cheapest, 'specialisation':specialisation}

#Endpoint 7:
@app.get('/doctors/filter')
def filter_doctors(specialization: Optional[str]=None, max_fee: Optional[int]=None, min_experience: Optional[int]=None, is_available: Optional[bool]=None):
    result=filter_doctors_logic(specialization, max_fee, min_experience, is_available)
    return {"total":len(result) ,"data":result}


#Endpoint 16:
@app.get("/doctors/search")
def search_doctors(keyword: str):
    result = [d for d in doctors if keyword.lower() in d["name"].lower() or keyword.lower() in d["specialization"].lower()]
    if not result:
        return {"message": "No doctors found matching keyword"}
    return {"total_found": len(result), "data": result}

#Endpoint 17:
@app.get("/doctors/sort")
def sort_doctors(sort_by: str = "fee"):
    if sort_by not in ["fee", "name", "experience_years"]:
        raise HTTPException(400, "Invalid sort field")
    return {"data": sorted(doctors, key=lambda x: x[sort_by])}

#Endpoint 18:
@app.get("/doctors/page")
def paginate_doctors(page: int = 1, limit: int = 3):
    total = len(doctors)
    total_pages = math.ceil(total / limit)
    start = (page - 1) * limit
    end = start + limit
    return {"page": page,"total_pages": total_pages,"data": doctors[start:end]}

#Endpoint 22:
@app.get("/doctors/browse")
def browse_doctors(keyword: Optional[str] = None,sort_by: str = "fee",order: str = "asc",page: int = 1,limit: int = 4):
    result = doctors
    if keyword: 
        result = [d for d in result if keyword.lower() in d["name"].lower() or keyword.lower() in d["specialization"].lower()]
    result = sorted(result, key=lambda x: x[sort_by], reverse=(order == "desc"))
    total = len(result)
    total_pages = math.ceil(total / limit)
    start = (page - 1) * limit
    end = start + limit
    return {"total": total,"total_pages": total_pages,"data": result[start:end]}

#Endpoint 3:
@app.get('/doctors/{doctor_id}')
def get_doctor(doctor_id:int):
    for doctor in doctors:
        if doctor['id']==doctor_id:
            return doctor
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")

#Endpoint 4:
appointments=[]
appt_counter=1
@app.get('/appointments')
def get_appointments():
    return {'total':len(appointments), 'appointments':appointments}

#Endpoint 6:
@app.post('/appointments')
def create_appointment(req: AppointmentRequest):
    global appt_counter
    doctor=find_doctor(req.doctor_id)
    if not doctor:
        raise HTTPException(404, "Doctor not found")
    if not doctor["is_available"]:
        return {"message":"Doctor is not available"}
    fee=calculate_fee(doctor["fee"], req.appointment_type, req.senior_citizen)
    appointment={
        "appointment_id":appt_counter,
        "patient":req.patient_name,
        "doctor_id":req.doctor_id,
        "doctor_name":doctor["name"],
        "date":req.date,
        "type":req.appointment_type,
        "status":"scheduled",
        **fee   
    }
    #aquired_fee=appointment["final_fee"]
    appointments.append(appointment)
    doctor["is_available"] = False
    appt_counter+=1
    return {"message":"Appointment created successfully", "appointment":appointment}



#Endpoint 8:
@app.post('/doctors')
def add_doctor(doctor:NewDoctor):
    for d in doctors:
        if d["name"].lower()==doctor.name.lower():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Doctor with this name already exists")
    new_doctor=doctor.dict()
    new_doctor["id"]=len(doctors)+1
    doctors.append(new_doctor)
    return {"message":"Doctor added successfully", "doctor":new_doctor}

#Endpoint 9:
@app.put('/doctors/{doctor_id}')
def update_doctor(doctor_id:int, fee: Optional[int] = None, is_available: Optional[bool] = None):
    doctor=find_doctor(doctor_id)
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    if fee is not None:
        doctor["fee"] = fee
    if is_available is not None:
        doctor["is_available"] = is_available
    return {"message":"Doctor updated successfully", "doctor":doctor}

#Endpoint 10:
@app.delete('/doctors/{doctor_id}')
def delete_doctor_by_id(doctor_id: int):
    doctor=find_doctor(doctor_id)
    if not doctor:
        raise HTTPException(404, "Doctor not found")
    for appointment in appointments:
        if appointment["doctor_id"]==doctor_id and appointment["status"] in ["scheduled","confirmed"]:
            raise HTTPException(400, "Cannot delete doctor with appointments")
    doctors.remove(doctor)
    return {"message":"Doctor deleted successfully"}

#Endpoint 11:
@app.post("/appointments/{appointment_id}/confirm")
def confirm_appointment(appointment_id:int):
    appointment=find_appointment(appointment_id)
    if not appointment:
        raise HTTPException(404, "Appointment not found")
    appointment["status"]="confirmed"
    return {"message":"Appointment confirmed successfully", "appointment":appointment}

#Endpoint 12:
@app.post("/appointments/{appointment_id}/cancel")
def cancel_appointment(appointment_id:int):
    appointment=find_appointment(appointment_id)
    if not appointment:
        raise HTTPException(404, "Appointment not found")
    appointment["status"]="cancelled"
    doctor=find_doctor(appointment["doctor_id"])
    if doctor:
        doctor["is_available"] = True
    return {"message":"Appointment cancelled successfully", "appointment":appointment}

#Endpoint 13:
@app.post("/appointments/{appointment_id}/complete")
def complete_appointment(appointment_id:int):
    appointment = find_appointment(appointment_id)
    if not appointment:
        raise HTTPException(404, "Appointment not found")
    appointment["status"] = "completed"
    return {"message": "Appointment completed", "data": appointment}

#Endpoint 14:
@app.get("/appointments/active")
def active_appointments():
    active = [a for a in appointments if a["status"] in ["scheduled", "confirmed"]]
    return {"total": len(active), "data": active}

#Endpoint 15:
@app.get("/appointments/by-doctor/{doctor_id}")
def appointments_by_doctor(doctor_id: int):
    result = [a for a in appointments if a["doctor_id"] == doctor_id]
    return {"total": len(result), "data": result}



#Endpoint 19:
@app.get("/appointments/search")
def search_appointments(patient_name: str):
    result = [a for a in appointments if patient_name.lower() in a["patient"].lower()]
    return {"total": len(result), "data": result}

#Endpoint 20:
@app.get("/appointments/sort")
def sort_appointments(sort_by: str = "final_fee"):
    if sort_by not in ["final_fee", "date"]:
        raise HTTPException(400, "Invalid sort field")
    return {"data": sorted(appointments, key=lambda x: x[sort_by])}

#Endpoint 21:
@app.get("/appointments/page")
def paginate_appointments(page: int = 1, limit: int = 3):
    total = len(appointments)
    total_pages = math.ceil(total / limit)
    start = (page - 1) * limit
    end = start + limit
    return {"page": page,"total_pages": total_pages,"data": appointments[start:end]}


