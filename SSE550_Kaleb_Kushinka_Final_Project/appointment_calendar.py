import tkinter as tk
import tkinter.messagebox as messagebox
from tkcalendar import Calendar
from datetime import datetime

class AppointmentCalendar:
    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.root = tk.Tk()
        self.root.title("Appointment Calendar")

        self.calendar = Calendar(self.root, selectmode='day')
        self.calendar.pack(pady=20)

        self.show_appointments_button = tk.Button(self.root, text="Show Appointments", command=self.show_appointments)
        self.show_appointments_button.pack(pady=10)

    def show_appointments(self):
        date = self.calendar.get_date()
        date_obj = datetime.strptime(date, '%m/%d/%y').date()
        appointments = self.scheduler.filter_appointments('date', str(date_obj))
        appointments_text = '\n'.join([str(appt) for appt in appointments]) if appointments else "No appointments on this date."
        messagebox.showinfo("Appointments", appointments_text)

    def run(self):
        self.root.mainloop()

    def close(self):
        self.root.destroy()

