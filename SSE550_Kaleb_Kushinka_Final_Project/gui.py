import tkinter as tk
from PIL import Image, ImageTk
from tkinter import  messagebox
from tkcalendar import Calendar
import datetime
from scheduler import Scheduler
from appointment import Appointment

class AppointmentApp:
    def __init__(self, master):
        self.master = master
        self.scheduler = Scheduler()  # Assuming you have a Scheduler class
        master.title("Dentist Appointment Scheduler")

        # Initialize the appointment_widgets attribute
        self.appointment_widgets = []

        # Welcome message label
        self.welcome_label = tk.Label(master, text="Welcome to the Dental Scheduler", font=("Arial", 16))
        self.welcome_label.pack(pady=10)

        # Load and display the image using Pillow
        self.image = Image.open("cartoon_dental.jpg")  # Replace with your image file path
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(master, image=self.photo)
        self.image_label.pack(pady=10)


        self.view_calendar_button = tk.Button(master, text="View Calendar", command=self.open_calendar)
        self.view_calendar_button.pack(pady=10)

    def generate_timeslots(self):
        start_time = datetime.datetime(2023, 1, 1, 8, 0)  # Using a base date
        end_time = datetime.datetime(2023, 1, 1, 16, 0)  # Up to 4:00 PM
        timeslots = []
        while start_time < end_time:
            timeslots.append(start_time.strftime("%I:%M %p"))
            start_time += datetime.timedelta(hours=1)
        return timeslots
    
    def get_booked_timeslots(self, date):
        appointments = self.scheduler.filter_appointments('date', date)
        return [appt.time for appt in appointments]  # Directly use the time string
    
    
    def get_date_statuses(self):
        appointments = self.scheduler.get_all_appointments()
        date_counts = {}
        for appt in appointments:
            date = appt.date
            date_counts[date] = date_counts.get(date, 0) + 1

        date_statuses = {}
        for date, count in date_counts.items():
            if count <= 1:
                date_statuses[date] = ('Full Availability', 'green')
            elif 2 <= count <= 3:
                date_statuses[date] = ('Limited Availability', 'yellow')
            else:
                date_statuses[date] = ('No Availability', 'red')
        return date_statuses
    
    
    def open_calendar(self):
        self.calendar_window = tk.Toplevel(self.master)
        self.calendar_window.title("View Calendar")


        self.calendar = Calendar(self.calendar_window, selectmode='day')
        self.calendar.pack(pady=10)

        # Button to schedule a new appointment
        self.add_appointment_button = tk.Button(self.calendar_window, text="Schedule Appointment", command=self.schedule_appointment_from_calendar)
        self.add_appointment_button.pack(pady=10)

        self.view_appointments_button = tk.Button(self.calendar_window, text="View Appointments", command=self.view_appointments_on_date)
        self.view_appointments_button.pack(pady=10)

        # Button to view and cancel appointments
        self.view_cancel_appointments_button = tk.Button(self.calendar_window, text="View & Cancel Appointments", command=self.open_appointment_cancellation_window)
        self.view_cancel_appointments_button.pack(pady=10)

        self.date_status_label = tk.Label(self.calendar_window, text="")
        self.date_status_label.pack(pady=10)

        
            

        self.calendar.bind("<<CalendarSelected>>", self.update_date_status)


        self.update_date_status()

    def open_appointment_cancellation_window(self):
        selected_date = self.calendar.get_date()
        formatted_date = datetime.datetime.strptime(selected_date, '%m/%d/%y').strftime('%Y-%m-%d')
        appointments = self.scheduler.filter_appointments('date', formatted_date)

        cancellation_window = tk.Toplevel(self.master)
        cancellation_window.title("Cancel Appointments on " + formatted_date)

        if not appointments:
            tk.Label(cancellation_window, text="No appointments to cancel for this day.").pack()
            return

        for appt in appointments:
            appt_label = tk.Label(cancellation_window, text=str(appt))
            cancel_button = tk.Button(cancellation_window, text="Cancel", command=lambda a=appt: self.cancel_appointment(a, cancellation_window))
            appt_label.pack()
            cancel_button.pack()
        
        

    def cancel_appointment(self, appointment, window):
        self.scheduler.cancel_appointment(appointment)
        window.destroy()  # Close the cancellation window
        
        # Refresh the calendar view
        self.refresh_calendar_availability()


    def refresh_calendar_availability(self):
        # Logic to refresh the calendar view and update availability
        # This might involve re-calling the method that initializes or updates the calendar view
        self.calendar_window.destroy()
        self.open_calendar() 

    def update_date_status(self, event=None):
        selected_date = self.calendar.get_date()
        formatted_date = datetime.datetime.strptime(selected_date, '%m/%d/%y').strftime('%Y-%m-%d')

        date_statuses = self.get_date_statuses()
        status_text, status_color = date_statuses.get(formatted_date, ('Full Availability', 'green'))

        self.date_status_label.config(text=f"Status: {status_text}", bg=status_color)
    
    def schedule_appointment_from_calendar(self):
        selected_date = self.calendar.get_date()
        # Convert the selected_date to a suitable format if necessary
        try:
            date_obj = datetime.datetime.strptime(selected_date, '%m/%d/%y').date()
            formatted_date = date_obj.strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Invalid date format")
            return

        self.schedule_window = tk.Toplevel(self.master)
        self.schedule_window.title("Schedule Appointment")

         # Get available timeslots
        formatted_date = datetime.datetime.strptime(selected_date, '%m/%d/%y').strftime('%Y-%m-%d')
        all_timeslots = self.generate_timeslots()
        booked_timeslots = self.get_booked_timeslots(formatted_date)
        available_timeslots = [ts for ts in all_timeslots if ts not in booked_timeslots]
        print("Available timeslots: {}".format(available_timeslots))

        # Dropdown for available timeslots
        self.time_var = tk.StringVar(self.schedule_window)
        if available_timeslots:
            self.time_var.set(available_timeslots[0])  # Set the default value
            self.time_dropdown = tk.OptionMenu(self.schedule_window, self.time_var, *available_timeslots)
            self.time_dropdown.pack()
        else:
            tk.Label(self.schedule_window, text="No available timeslots.").pack()

        # Date label and entry (pre-filled with formatted date)
        tk.Label(self.schedule_window, text="Date:").pack()
        self.date_entry = tk.Entry(self.schedule_window)
        self.date_entry.insert(0, formatted_date)  # Pre-fill with the formatted date
        self.date_entry.pack()


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
        selected_time_str = self.time_var.get()
        date_str = self.date_entry.get()
        patient_name = self.patient_name_entry.get()
        appointment_type = self.appointment_type_entry.get()
        doctor_name = self.doctor_entry.get()


        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        try:
            time_obj = datetime.datetime.strptime(selected_time_str, "%I:%M %p").time()
            formatted_time = time_obj.strftime("%I:%M %p")
        except ValueError:
            messagebox.showerror("Error", "Invalid time format. Please use HH:MM AM/PM.")
            return

        
        

        # Create the appointment and add it to the schedule
        appointment = Appointment(None, date, formatted_time, patient_name, appointment_type, doctor_name)
        result = self.scheduler.add_appointment(appointment)
        messagebox.showinfo("Appointment", result)
        if result.startswith("Appointment scheduled"):
            self.schedule_window.destroy()
            self.refresh_appointments_list()  # Refresh the list if needed
    
    def filter_appointments(self, filter_type, filter_value):
        filtered = []
        current = self.head
        while current:
            appt = current.appointment
            if filter_type == 'date':
            # Compare in a consistent format, e.g., 'YYYY-MM-DD'
                appt_date = appt.date.strftime('%Y-%m-%d')
                if appt_date == filter_value:
                    filtered.append(appt)
            # ... other filter conditions ...
            current = current.next
        return filtered

    def view_appointments_on_date(self):
        selected_date = self.calendar.get_date()
        formatted_date = datetime.datetime.strptime(selected_date, '%m/%d/%y').strftime('%Y-%m-%d')
        appointments = self.scheduler.filter_appointments('date', formatted_date)

        appointment_window = tk.Toplevel(self.master)
        appointment_window.title("Appointments on " + formatted_date)

        # Map appointments to their time slots
        appt_by_time = {appt.time: appt for appt in appointments}

        for timeslot in self.generate_timeslots():
            appt = appt_by_time.get(timeslot)
            if appt:
                appt_details = tk.Label(appointment_window, text=f"{timeslot}: {appt.appointment_type} Appointment for {appt.patient_name} with Doctor {appt.doctor_name}")
                appt_details.pack()
            else:
                appt_details = tk.Label(appointment_window, text=f"{timeslot}: No current appointment.")
                appt_details.pack()


        if not appointments:
            tk.Label(appointment_window, text="No appointments for this day.").pack()
            

    def refresh_appointments_list(self):
        # Check if there are any widgets to clear
        if hasattr(self, 'appointment_widgets'):
            for widget in self.appointment_widgets:
                widget.destroy()
            self.appointment_widgets.clear()

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