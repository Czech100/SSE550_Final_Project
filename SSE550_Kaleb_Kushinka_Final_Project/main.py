import datetime
from gui import run_app
from appointment import Appointment
from appointment_calendar import AppointmentCalendar

def parse_date(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

def parse_time(time_str):
    return datetime.datetime.strptime(time_str, "%H:%M").time()

def get_user_input(scheduler):
    date_str = input("Enter the date for the appointment (YYYY-MM-DD): ")
    time_str = input("Enter the time for the appointment (HH:MM): ")
    patient_name = input("Enter the patient's name: ")
    doctor_name = input("Enter the Doctor's name: ")
    appointment_type = input("Enter the type of appointment: ")


    try:
        date = parse_date(date_str)
        time = parse_time(time_str)
    except ValueError:
        return "Invalid date or time format. Please try again."

    appointment = Appointment(None, date, time, patient_name, doctor_name, appointment_type)
    return scheduler.add_appointment(appointment)

def cancel_user_appointment_by_name_or_id(scheduler):
    identifier = input("Enter the patient's name or ID to cancel their appointment: ")
    return scheduler.cancel_appointment_by_name_or_id(identifier)

def show_calendar(scheduler):
    appointment_calendar = AppointmentCalendar(scheduler)
    appointment_calendar.run()

def is_valid_name(name):
    return name.isalpha()

def is_valid_date(date_str):
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        return True
    except ValueError:
        return False

def main_menu():
    print("\n--- Dentist Appointment Scheduler ---")
    print("1. Schedule a new appointment")
    print("2. View all appointments")
    print("3. Cancel an appointment")
    print("4. Show Calendar")
    print("5. Quit")
    choice = input("Enter your choice (1-5): ")
    return choice

def view_appointments_submenu(scheduler):
    print("\nWhat appointments would you liek to view?")
    print("1. View by appointment type")
    print("2. View by patient name")
    print("3. View by doctor")
    print("4. View by date")
    print("5. Return to main menu")
    choice = input("Enter your choice (1-5): ")

    if choice == '1':
        appointment_type = input("Enter appointment type: ")
        appointments = scheduler.filter_appointments('type', appointment_type)
    elif choice == '2':
        patient_name = input("Enter patient name: ")
        if not is_valid_name(patient_name):
            print("Invalid name. Names should contain only letters.")
            return
        appointments = scheduler.filter_appointments('patient', patient_name)
    elif choice == '3':
        doctor = input("Enter doctor name: ")
        if not is_valid_name(doctor):
            print("Invalid name. Names should contain only letters.")
            return
        appointments = scheduler.filter_appointments('doctor', doctor)
    elif choice == '4':
        date_input = input("Enter date (YYYY-MM-DD): ")
        if not is_valid_date(date_input):
            print("Invalid date format. Please use YYYY-MM-DD.")
            return
        date = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
        appointments = scheduler.filter_appointments('date', date)
    elif choice == '5':
        return
    else:
        print("Invalid choice. Please enter a number between 1 and 5.")
        return

    if appointments:
        for appt in appointments:
            print(appt)
    else:
        print("No appointments found for this filter.")

def main():
    run_app()

if __name__ == "__main__":
    main()
