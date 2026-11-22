from app import Doctor, Appointment, db
from patterns.user_factory import UserFactory
from patterns.observer import AppointmentSubject

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"CarePoint" in response.data

def test_doctor_api(client):
    response = client.get("/api/doctors")
    assert response.status_code == 200
    assert response.json[0]["specialization"] == "Cardiology"

def test_appointment_booking_and_duplicate_rejection(client, app):
    data = {
        "patient_name": "Demo Patient", "patient_email": "demo@example.com",
        "doctor_id": "1", "appointment_date": "2026-12-10",
        "appointment_time": "10:00"
    }
    first = client.post("/book", data=data, follow_redirects=True)
    assert b"created" in first.data
    second = client.post("/book", data=data, follow_redirects=True)
    assert b"already has an appointment" in second.data

def test_user_factory():
    user = UserFactory.create("patient", "Demo", "demo@example.com")
    assert user.role == "patient"

def test_observer_pattern():
    received = []
    class Recorder:
        def update(self, message):
            received.append(message)
    subject = AppointmentSubject()
    subject.attach(Recorder())
    subject.notify("Appointment confirmed")
    assert received == ["Appointment confirmed"]
