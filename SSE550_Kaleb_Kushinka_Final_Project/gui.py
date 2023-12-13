import tkinter as tk
from PIL import Image, ImageTk
from tkinter import  messagebox
from tkcalendar import Calendar
from datetime import datetime
from scheduler import Scheduler
from appointment import Appointment

class AppointmentApp:
    def __init__(self, master):
        self.master = master
        self.scheduler = Scheduler()  # Assuming you have a Scheduler class
        master.title("Dentist Appointment Scheduler")

        # Welcome message label
        self.welcome_label = tk.Label(master, text="Welcome to the Dental Scheduler", font=("Arial", 16))
        self.welcome_label.pack(pady=10)

        # Load and display the image using Pillow
        self.image = Image.open("cartoon_dental.jpg")  # Replace with your image file path
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(master, image=self.photo)
        self.image_label.pack(pady=10)

        self.add_appointment_button = tk.Button(master, text="Schedule Appointment", command=self.open_schedule_dialog)
        self.add_appointment_button.pack()

        self.view_appointments_button = tk.Button(master, text="View Appointments", command=self.open_view_dialog)
        self.view_appointments_button.pack()

        self.view_calendar_button = tk.Button(master, text="View Calendar", command=self.open_calendar)
        self.view_calendar_button.pack(pady=10)

    def open_schedule_dialog(self):
        self.schedule_window = tk.Toplevel(self.master)
        self.schedule_window.title("Schedule an Appointment")

        # Form fields
        tk.Label(self.schedule_window, text="Date (YYYY-MM-DD):").pack()
        self.date_entry = tk.Entry(self.schedule_window)
        self.date_entry.pack()

        tk.Label(self.schedule_window, text="Time (HH:MM):").pack()
        self.time_entry = tk.Entry(self.schedule_window)
        self.time_entry.pack()

        tk.Label(self.schedule_window, text="Patient Name:").pack()
        self.patient_name_entry = tk.Entry(self.schedule_window)
        self.patient_name_entry.pack()

        tk.Label(self.schedule_window, text="Doctor:").pack()
        self.appointment_type_entry = tk.Entry(self.schedule_window)
        self.appointment_type_entry.pack()

        tk.Label(self.schedule_window, text="Appointment Type:").pack()
        self.doctor_entry = tk.Entry(self.schedule_window)
        self.doctor_entry.pack()

        # Schedule button
        self.schedule_button = tk.Button(self.schedule_window, text="Schedule", command=self.schedule_appointment)
        self.schedule_button.pack()

    def schedule_appointment(self):
        # Get user input
        date_str = self.date_entry.get()
        time_str = self.time_entry.get()
        patient_name = self.patient_name_entry.get()
        appointment_type = self.appointment_type_entry.get()
        doctor = self.doctor_entry.get()

        # Convert date and time
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            time = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            messagebox.showerror("Error", "Invalid date or time format")
            return

        # Create appointment object
        appointment = Appointment(None, date, time, patient_name, appointment_type, doctor)
        
        # Check for conflicts and schedule if no conflict
        result = self.scheduler.add_appointment(appointment)
        messagebox.showinfo("Result", result)
        if result == "Appointment scheduled.":
            self.schedule_window.destroy()

    def open_view_dialog(self):
        self.view_window = tk.Toplevel(self.master)
        self.view_window.title("View Appointments")

        # Drop-down menu for choosing filter type
        self.filter_var = tk.StringVar(self.view_window)
        self.filter_var.set("doctor")  # default value
        self.filter_option_menu = tk.OptionMenu(self.view_window, self.filter_var, "doctor", "date", "type", "name")
        self.filter_option_menu.pack()

        # Entry field for filter value
        tk.Label(self.view_window, text="Enter filter value:").pack()
        self.filter_value_entry = tk.Entry(self.view_window)
        self.filter_value_entry.pack()

        # Button to perform the search
        self.search_button = tk.Button(self.view_window, text="Search", command=self.view_appointments)
        self.search_button.pack()

    def view_appointments(self):
        filter_type = self.filter_var.get()
        filter_value = self.filter_value_entry.get()

        # Assuming your Scheduler class has a method filter_appointments(filter_type, filter_value)
        appointments = self.scheduler.filter_appointments(filter_type, filter_value)
        appointments_text = '\n'.join([str(appt) for appt in appointments]) if appointments else "No appointments found."

        # Display the result in a message box or another appropriate widget
        messagebox.showinfo("Appointments", appointments_text)
    def open_calendar(self):
        self.calendar_window = tk.Toplevel(self.master)
        self.calendar_window.title("View Calendar")

        self.calendar = Calendar(self.calendar_window, selectmode='day')
        self.calendar.pack(pady=10)

        self.view_appointments_button = tk.Button(self.calendar_window, text="View Appointments", command=self.view_appointments_on_date)
        self.view_appointments_button.pack(pady=10)

        # Button to schedule a new appointment
        self.add_appointment_button = tk.Button(self.calendar_window, text="Schedule Appointment", command=self.schedule_appointment_from_calendar)
        self.add_appointment_button.pack(pady=10)
    
    def schedule_appointment_from_calendar(self):
        selected_date = self.calendar.get_date()
        # Convert the selected_date to a suitable format if necessary

        self.schedule_window = tk.Toplevel(self.master)
        self.schedule_window.title("Schedule Appointment")

        # Date label and entry (pre-filled with selected date)
        tk.Label(self.schedule_window, text="Date:").pack()
        self.date_entry = tk.Entry(self.schedule_window)
        self.date_entry.insert(0, selected_date)  # Pre-fill with the selected date
        self.date_entry.pack()

        # Time entry
        tk.Label(self.schedule_window, text="Time (HH:MM):").pack()
        self.time_entry = tk.Entry(self.schedule_window)
        self.time_entry.pack()

        # Patient name entry
        tk.Label(self.schedule_window, text="Patient Name:").pack()
        self.patient_name_entry = tk.Entry(self.schedule_window)
        self.patient_name_entry.pack()

        # Appointment type entry
        tk.Label(self.schedule_window, text="Appointment Type:").pack()
        self.appointment_type_entry = tk.Entry(self.schedule_window)
        self.appointment_type_entry.pack()

        # Doctor name entry
        tk.Label(self.schedule_window, text="Doctor:").pack()
        self.doctor_entry = tk.Entry(self.schedule_window)
        self.doctor_entry.pack()

        # Schedule button
        self.schedule_button = tk.Button(self.schedule_window, text="Schedule", command=self.add_appointment)
        self.schedule_button.pack()


    def add_appointment(self):
        # Extract data from the entry fields
        date_str = self.date_entry.get()
        time_str = self.time_entry.get()
        patient_name = self.patient_name_entry.get()
        appointment_type = self.appointment_type_entry.get()
        doctor = self.doctor_entry.get()

        # Convert date and time from string to appropriate format
        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            time = datetime.datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            messagebox.showerror("Error", "Invalid date or time format")
            return

        # Create the appointment and add it to the schedule
        appointment = Appointment(None, date, time, patient_name, appointment_type, doctor)
        result = self.scheduler.add_appointment(appointment)
        messagebox.showinfo("Appointment", result)
        if result.startswith("Appointment scheduled"):
            self.schedule_window.destroy()
            self.refresh_appointments_list()  # Refresh the list if needed
    
    def view_appointments_on_date(self):
        selected_date = self.calendar.get_date()
        # Convert selected_date to a suitable format if necessary
        appointments = self.scheduler.filter_appointments('date', selected_date)

        if not appointments:
            messagebox.showinfo("Appointments on " + selected_date, "No appointments on this date.")
            return

        # Create a new window to list appointments with cancel buttons
        self.appointment_list_window = tk.Toplevel(self.calendar_window)
        self.appointment_list_window.title("Appointments on " + selected_date)

        self.appointment_widgets = []  # List to store appointment widgets

        for appt in appointments:
            appt_label = tk.Label(self.appointment_list_window, text=str(appt))
            appt_label.pack()
            self.appointment_widgets.append(appt_label)
            cancel_button = tk.Button(self.appointment_list_window, text="Cancel", 
                                      command=lambda appt_id=appt.patient_id: self.cancel_appointment(appt_id))
            cancel_button.pack()
            self.appointment_widgets.append(cancel_button)

    def cancel_appointment(self, appointment_id):
        result = self.scheduler.cancel_appointment_by_id(appointment_id)
        messagebox.showinfo("Cancellation Result", result)
        self.refresh_appointments_list()  # Refresh the list of appointments

    def refresh_appointments_list(self):
        # Clear existing appointment widgets
        for widget in self.appointment_widgets:
            widget.destroy()

        # Repopulate the list with updated appointments
        selected_date = self.calendar.get_date()
        appointments = self.scheduler.filter_appointments('date', selected_date)

        for appt in appointments:
            appt_label = tk.Label(self.appointment_list_window, text=str(appt))
            appt_label.pack()
            self.appointment_widgets.append(appt_label)

            cancel_button = tk.Button(self.appointment_list_window, text="Cancel", 
                                      command=lambda appt_id=appt.patient_id: self.cancel_appointment(appt_id))
            cancel_button.pack()
            self.appointment_widgets.append(cancel_button)
def run_app():
    root = tk.Tk()
    app = AppointmentApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_app()