import datetime
class Appointment:
    def __init__(self, patient_id, date, time, patient_name,appointment_type,doctor_name):
        self.patient_id = patient_id
        self.date = date
        self.time = time
        self.patient_name = patient_name
        self.appointment_type = appointment_type
        self.doctor_name = doctor_name

    def __str__(self):
        try:
            # Attempt to parse the time string into a datetime.time object
            formatted_time = datetime.datetime.strptime(self.time, "%H:%M").strftime("%I:%M %p")
        except (ValueError, TypeError):
            # If parsing fails, use the original time string
            formatted_time = self.time
        return f"ID: {self.patient_id}, Date: {self.date}, Time: {formatted_time}, Patient: {self.patient_name},Doctor: {self.doctor_name}, Type: {self.appointment_type}"
