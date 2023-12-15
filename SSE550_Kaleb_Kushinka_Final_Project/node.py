class Node:
    #Class for storing the data of the appointments
    def __init__(self, appointment):
        self.appointment = appointment
        self.next = None