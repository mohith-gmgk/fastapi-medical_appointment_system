# Medical Appointment System (FastAPI)

A simple backend system built using FastAPI to manage doctors, appointments, and consultation workflows.

This project simulates a real-world clinic system where users can:

* View doctors
* Book appointments
* Manage appointment lifecycle
* Search, filter, and paginate data

---

## Features

### Doctor Management

* View all doctors
* Get doctor by ID
* Add new doctors
* Update doctor details
* Delete doctors with safety checks

### Appointment System

* Book appointments with validation
* Automatic fee calculation based on appointment type
* Senior citizen discounts
* Track appointment status:

  * Scheduled
  * Confirmed
  * Cancelled
  * Completed

### Workflow Handling

* Confirm appointment
* Cancel appointment (doctor becomes available again)
* Complete appointment

### Advanced Query Features

* Filter doctors by:

  * Specialization
  * Fee
  * Experience
  * Availability
* Search doctors and appointments
* Sort results
* Pagination support
* Combined browsing (search, sort, and pagination)

---

## Tech Stack

* FastAPI for building APIs
* Pydantic for data validation
* Python as the programming language
* Uvicorn as the server

---

## Project Structure

```
main.py   # Contains all endpoints and logic
```

---

## Installation and Setup

### 1. Clone the repository

```bash
git clone <your-repo-link>
cd medical-appointment-system
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the server

```bash
uvicorn main:app --reload
```

### 4. Open API documentation

```
http://127.0.0.1:8000/docs
```

---

## Example Endpoints

### Get all doctors

```
GET /doctors
```

### Book an appointment

```
POST /appointments
```

### Filter doctors

```
GET /doctors/filter?specialization=Cardiologist&max_fee=500
```

### Appointment workflow

```
POST /appointments/{id}/confirm
POST /appointments/{id}/cancel
POST /appointments/{id}/complete
```

---

## Key Learnings

This project demonstrates:

* REST API design
* Data validation using Pydantic
* CRUD operations
* Business logic implementation
* Query parameters and filtering
* Pagination and sorting
* Workflow-based API design

---

## Notes

* This project uses in-memory data and does not persist data
* Data will reset when the server restarts
* Can be extended with a database such as SQLite or PostgreSQL

---

## Future Improvements

* Add database integration using SQLAlchemy
* Implement authentication using JWT
* Organize code into routers and services
* Add logging and error handling middleware

---

## Author

Developed as part of a 6-day FastAPI backend training project focused on building strong API development skills.
