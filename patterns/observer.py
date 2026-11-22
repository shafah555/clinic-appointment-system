class AppointmentSubject:
    """Behavioral Observer pattern: notifies subscribed observers of a change."""
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def notify(self, message):
        for observer in self.observers:
            observer.update(message)

class ConsoleNotificationObserver:
    def update(self, message):
        print(f"[DEMO NOTIFICATION] {message}")
