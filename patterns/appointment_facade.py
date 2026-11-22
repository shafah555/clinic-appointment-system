
class AppointmentFacade:
    """Structural pattern: gives the booking workflow one simple interface."""

    def __init__(self, session, notifier):
        self.session = session
        self.notifier = notifier

    def book(self, patient_name, patient_email, doctor, date, time):
        # Import Appointment locally to avoid a circular import.
        from app import Appointment

        exists = self.session.query(Appointment).filter_by(
            doctor_id=doctor.id,
            appointment_date=date,
            appointment_time=time
        ).first()

        if exists:
            raise ValueError(
                "That doctor already has an appointment at this time."
            )

        appointment = Appointment(
            patient_name=patient_name,
            patient_email=patient_email,
            doctor_id=doctor.id,
            appointment_date=date,
            appointment_time=time,
            status="Pending"
        )

        self.session.add(appointment)
        self.notifier(
            patient_email,
            "Your appointment request was received."
        )

        return appointment
