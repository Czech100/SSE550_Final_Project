class Appointment:
    def __init__(self, patient_id, date, time, patient_name,doctor_name, appointment_type):
        self.patient_id = patient_id
        self.date = date
        self.time = time
        self.patient_name = patient_name
        self.doctor_name = doctor_name
        self.appointment_type = appointment_type

    def __str__(self):
        formatted_time = self.time.strftime("%I:%M %p")
        return f"ID: {self.patient_id}, Date: {self.date}, Time: {formatted_time}, Patient: {self.patient_name},Doctor: {self.doctor_name}, Type: {self.appointment_type}"
