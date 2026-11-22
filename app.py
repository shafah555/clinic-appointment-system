import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from werkzeug.security import generate_password_hash
from patterns.user_factory import UserFactory
from patterns.appointment_facade import AppointmentFacade
from patterns.observer import AppointmentSubject, ConsoleNotificationObserver

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    fee = db.Column(db.Float, nullable=False, default=500)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    patient_email = db.Column(db.String(120), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"), nullable=False)
    appointment_date = db.Column(db.String(10), nullable=False)
    appointment_time = db.Column(db.String(5), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Pending")
    doctor = db.relationship("Doctor", backref="appointments")
    __table_args__ = (
        UniqueConstraint("doctor_id", "appointment_date", "appointment_time",
                         name="uq_doctor_date_time"),
    )

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointment.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(20), default="Unpaid")
    appointment = db.relationship("Appointment", backref=db.backref("bill", uselist=False))

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.String(120), nullable=False)
    message = db.Column(db.String(250), nullable=False)
    status = db.Column(db.String(20), default="Unread")

def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "assignment-demo-secret-change-me")
    database_url = os.getenv("DATABASE_URL", "sqlite:///clinic_demo.db")
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    # Neon requires SSL; SQLAlchemy/psycopg can use this connection option.
    if database_url.startswith("postgresql://") and "sslmode=" not in database_url:
        database_url += ("&" if "?" in database_url else "?") + "sslmode=require"
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    if test_config:
        app.config.update(test_config)
    db.init_app(app)

    @app.route("/")
    def index():
        doctors = Doctor.query.order_by(Doctor.name).all()
        appointments = Appointment.query.order_by(Appointment.id.desc()).limit(5).all()
        return render_template("index.html", doctors=doctors, appointments=appointments)

    @app.route("/doctors")
    def doctors():
        term = request.args.get("q", "").strip()
        query = Doctor.query
        if term:
            query = query.filter(Doctor.specialization.ilike(f"%{term}%"))
        return render_template("doctors.html", doctors=query.order_by(Doctor.name).all(), term=term)

    @app.route("/book", methods=["GET", "POST"])
    def book():
        doctors = Doctor.query.order_by(Doctor.name).all()
        if request.method == "POST":
            name = request.form.get("patient_name", "").strip()
            email = request.form.get("patient_email", "").strip()
            doctor_id = request.form.get("doctor_id", type=int)
            date = request.form.get("appointment_date", "")
            time = request.form.get("appointment_time", "")
            doctor = db.session.get(Doctor, doctor_id) if doctor_id else None
            if not all([name, email, doctor, date, time]):
                flash("Please complete every field.", "error")
                return render_template("book.html", doctors=doctors)
            facade = AppointmentFacade(db.session, notify)
            try:
                appointment = facade.book(name, email, doctor, date, time)
                db.session.commit()
                flash(f"Appointment #{appointment.id} created (Pending).", "success")
                return redirect(url_for("appointments"))
            except ValueError as exc:
                db.session.rollback()
                flash(str(exc), "error")
        return render_template("book.html", doctors=doctors)

    @app.route("/appointments")
    def appointments():
        rows = Appointment.query.order_by(Appointment.appointment_date.desc()).all()
        return render_template("appointments.html", appointments=rows)

    @app.post("/appointments/<int:appointment_id>/status")
    def update_status(appointment_id):
        appointment = db.session.get(Appointment, appointment_id)
        if not appointment:
            flash("Appointment not found.", "error")
            return redirect(url_for("appointments"))
        status = request.form.get("status")
        if status not in {"Confirmed", "Cancelled", "Completed"}:
            flash("Invalid status.", "error")
        else:
            appointment.status = status
            notify(appointment.patient_email, f"Appointment #{appointment.id}: {status}")
            db.session.commit()
            flash("Appointment status updated.", "success")
        return redirect(url_for("appointments"))

    @app.route("/billing")
    def billing():
        rows = Appointment.query.order_by(Appointment.id.desc()).all()
        return render_template("billing.html", appointments=rows)

    @app.post("/billing/<int:appointment_id>")
    def create_bill(appointment_id):
        appointment = db.session.get(Appointment, appointment_id)
        if not appointment:
            flash("Appointment not found.", "error")
        elif not appointment.bill:
            db.session.add(Bill(appointment_id=appointment.id, amount=appointment.doctor.fee))
            db.session.commit()
            flash("Invoice created.", "success")
        return redirect(url_for("billing"))

    @app.route("/notifications")
    def notifications():
        return render_template("notifications.html",
                               notifications=Notification.query.order_by(Notification.id.desc()).all())

    @app.route("/api/doctors")
    def api_doctors():
        return jsonify([{"id": d.id, "name": d.name, "specialization": d.specialization,
                         "fee": d.fee} for d in Doctor.query.order_by(Doctor.name).all()])

    @app.route("/api/appointments", methods=["GET"])
    def api_appointments():
        return jsonify([{"id": a.id, "patient": a.patient_name, "doctor": a.doctor.name,
                         "date": a.appointment_date, "time": a.appointment_time,
                         "status": a.status} for a in Appointment.query.all()])

    @app.cli.command("init-db")
    def init_db():
        db.create_all()
        if Doctor.query.count() == 0:
            db.session.add_all([
                Doctor(name="Dr. Ayesha Rahman", specialization="Cardiology", fee=800),
                Doctor(name="Dr. Tanvir Hasan", specialization="Dermatology", fee=600),
                Doctor(name="Dr. Nusrat Jahan", specialization="Medicine", fee=500),
                Doctor(name="Dr. Farhan Kabir", specialization="Pediatrics", fee=550),
            ])
            db.session.commit()
        print("Database initialized with demo doctors.")

    return app

def notify(recipient, message):
    subject = AppointmentSubject()
    subject.attach(ConsoleNotificationObserver())
    subject.attach(lambda_observer(recipient))
    subject.notify(message)
    db.session.add(Notification(recipient=recipient, message=message))

def lambda_observer(recipient):
    class DatabaseNotificationObserver:
        def update(self, message):
            # Persistence is handled by notify() after the observers run.
            pass
    return DatabaseNotificationObserver()

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if Doctor.query.count() == 0:
            db.session.add_all([
                Doctor(name="Dr. Ayesha Rahman", specialization="Cardiology", fee=800),
                Doctor(name="Dr. Tanvir Hasan", specialization="Dermatology", fee=600),
                Doctor(name="Dr. Nusrat Jahan", specialization="Medicine", fee=500),
            ])
            db.session.commit()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
