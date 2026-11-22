class Patient:
    def __init__(self, name, email):
        self.name, self.email, self.role = name, email, "patient"

class DoctorUser:
    def __init__(self, name, email):
        self.name, self.email, self.role = name, email, "doctor"

class Admin:
    def __init__(self, name, email):
        self.name, self.email, self.role = name, email, "admin"

class UserFactory:
    """Creational pattern: centralizes creation of role-specific user objects."""
    @staticmethod
    def create(role, name, email):
        classes = {"patient": Patient, "doctor": DoctorUser, "admin": Admin}
        if role not in classes:
            raise ValueError("Unknown user role")
        return classes[role](name, email)
