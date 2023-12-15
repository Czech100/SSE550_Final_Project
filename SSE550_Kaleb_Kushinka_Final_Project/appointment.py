import datetime
class Appointment:
    #Class definition (OOP concept)
    def __init__(self, patient_id, date, time, patient_name,appointment_type,doctor_name):
        # Constructor method to initialize the Appointment object (Encapsulation)
        # Variables (patient_id, date, etc.) are used to store appointment details
        self.patient_id = patient_id #Numeric data type
        self.date = date # String data type representing date
        self.time = time # String data type representing time
        self.patient_name = patient_name
        self.appointment_type = appointment_type
        self.doctor_name = doctor_name

    def __str__(self):
        # Special method to provide a string representation of the object

        # Exception handling using try-except
        try:
            # Attempt to parse the time string into a datetime.time object
            formatted_time = datetime.datetime.strftime(self.time, "%I:%M %p")
        except (ValueError, TypeError):
            # If parsing fails, use the original time string
            formatted_time = self.time
        return f"ID: {self.patient_id}, Date: {self.date}, Time: {formatted_time}, Patient: {self.patient_name}, Type: {self.appointment_type},Doctor: {self.doctor_name}"
