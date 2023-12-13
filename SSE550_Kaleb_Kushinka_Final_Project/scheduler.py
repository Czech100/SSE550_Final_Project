import json
from appointment import Appointment
from node import Node

class Scheduler:
    def __init__(self, filename='appointments.json'):
        self.filename = filename
        self.head = None
        self.last_patient_id = 0
        self.load_appointments()

    def load_appointments(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                for appt in reversed(data):
                    loaded_appointment = Appointment(appt['patient_id'], appt['date'], appt['time'],
                                                     appt['patient_name'],appt['doctor_name'], appt['appointment_type'])
                    self.add_appointment(loaded_appointment, load=True)
                    self.last_patient_id = max(self.last_patient_id, appt['patient_id'])
        except (FileNotFoundError, json.JSONDecodeError):
            self.head = None
    
    def filter_appointments(self, filter_by, value):
        filtered = []
        current = self.head
        while current:
            appointment = current.appointment
            if ((filter_by == 'type' and appointment.appointment_type == value) or
                (filter_by == 'patient' and appointment.patient_name == value) or
                (filter_by == 'doctor' and appointment.doctor == value) or
                (filter_by == 'date' and appointment.date == value)):
                filtered.append(appointment)
            current = current.next
        return filtered

    def save_appointments(self):
        appointments = []
        current = self.head
        while current:
            appointments.append(current.appointment.__dict__)
            current = current.next
        with open(self.filename, 'w') as file:
            json.dump(appointments, file, default=str)

    def add_appointment(self, appointment, load=False):
        if self.is_conflict(appointment):
            return "Conflict! This time slot is already booked."
        
        if not load:
            self.last_patient_id += 1
            appointment.patient_id = self.last_patient_id
        new_node = Node(appointment)
        if self.head is None:
            self.head = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        if not load:
            self.save_appointments()

        return "Appointment scheduled."

    def is_conflict(self, new_appointment):
        current = self.head
        while current:
            appt = current.appointment
            if (appt.date == new_appointment.date and appt.time == new_appointment.time):
                return True
            current = current.next
        return False
    
    def search_appointments(self, patient_name):
        current = self.head
        results = []
        while current:
            if current.appointment.patient_name.lower() == patient_name.lower():
                results.append(current.appointment)
            current = current.next
        return results
    
    def cancel_appointment_by_name_or_id(self, identifier):
        current = self.head
        previous = None
        found = False

        while current:
            is_id = identifier.isdigit()  # Check if the identifier is an ID
            appointment_matches = ((is_id and current.appointment.patient_id == int(identifier)) or
                                   (not is_id and current.appointment.patient_name.lower() == identifier.lower()))

            if appointment_matches:
                found = True
                if previous:
                    previous.next = current.next
                else:
                    self.head = current.next
                break  # Remove this break if you want to cancel all matching appointments
            previous = current
            current = current.next

        if found:
            self.save_appointments()
            return "Appointment canceled."
        else:
            return "No appointment found for the specified identifier."

    def view_appointments(self):
        current = self.head
        while current:
            print(current.appointment)
            current = current.next
    
    def filter_appointments(self, filter_type, filter_value):
        filtered = []
        current = self.head
        while current:
            appt = current.appointment
            if ((filter_type == 'doctor' and appt.doctor == filter_value) or
                (filter_type == 'date' and str(appt.date) == filter_value) or
                (filter_type == 'type' and appt.appointment_type == filter_value) or
                (filter_type == 'name' and appt.patient_name == filter_value)):
                filtered.append(appt)
            current = current.next
        return filtered
