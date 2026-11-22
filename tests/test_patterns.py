from unittest.mock import Mock
from patterns.appointment_facade import AppointmentFacade


def test_facade_uses_mocked_database_and_notification_dependencies():
    # Mock the external persistence layer so this unit test needs no real DB.
    session = Mock()
    session.query.return_value.filter_by.return_value.first.return_value = None
    notifier = Mock()
    doctor = Mock(id=17)

    facade = AppointmentFacade(session, notifier)
    appointment = facade.book(
        "Demo Patient", "demo@example.com", doctor, "2026-12-10", "10:30"
    )

    assert appointment.patient_name == "Demo Patient"
    assert appointment.status == "Pending"
    session.add.assert_called_once_with(appointment)
    notifier.assert_called_once_with(
        "demo@example.com", "Your appointment request was received."
    )
