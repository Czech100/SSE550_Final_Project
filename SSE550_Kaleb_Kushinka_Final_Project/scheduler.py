import json
from appointment import Appointment
from node import Node

class Scheduler:
    #Class to manage appointments
    def __init__(self, filename='appointments.json'):

        #Encapsulated data
        self.filename = filename
        self.head = None
        self.last_patient_id = 0
        self.load_appointments()

        # Initialize the appointments list
        self.appointments = []

    def load_appointments(self):
        #File operations: Reading from a JSON file
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                #... load data into linked list ...
                for appt in reversed(data):
                    loaded_appointment = Appointment(appt['patient_id'], appt['date'], appt['time'],
                                                     appt['patient_name'],appt['appointment_type'],appt['doctor_name'])
                    self.add_appointment(loaded_appointment, load=True)
                    self.last_patient_id = max(self.last_patient_id, appt['patient_id'])
        except (FileNotFoundError, json.JSONDecodeError):
            self.head = None

    
    def get_all_appointments(self):
        #Uses a while loop to get all the scheduled appointments
        current = self.head
        appointments = []
        while current:
            appointments.append(current.appointment)
            current = current.next
        return appointments
    


    def save_appointments(self):
        #saves the appointment by writing the appointment into the JSON file
        current = self.head
        while current:
            self.appointments.append(current.appointment.__dict__)
            current = current.next
        with open(self.filename, 'w') as file:
            json.dump(self.appointments, file, default=str)

    def add_appointment(self, appointment, load=False):
        #Adds appointment to appointment list
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
        #Used to check for appointment conflicts and lets the user know
        current = self.head
        while current:
            appt = current.appointment
            if (appt.date == new_appointment.date and appt.time == new_appointment.time):
                return True
            current = current.next
        return False
    
    def cancel_appointment(self, appointment_to_cancel):
        #Used to cancel/remove appointment from the scheduled appointment list
        current = self.head
        previous = None

        while current is not None:
            if current.appointment.time == appointment_to_cancel.time:
                if previous is None:
                    self.head = current.next  # Remove the head appointment
                else:
                    previous.next = current.next  # Remove appointment from the middle or end
                break
            previous = current
            current = current.next

        self.save_appointments()

    def filter_appointments(self, filter_type, filter_value):
        #Used to filter the appointments within the appointment list
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
