#!/usr/bin/env python3

__author__ = 'speky'
import alberlet
from alberlet import *
import tkinter
from tkinter import *

from geopy.geocoders import Nominatim
from geopy.distance import vincenty


class Gui(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("Awsome kereso")
        # get screen width and height
        ws = self.master.winfo_screenwidth()  # This value is the width of the screen
        hs = self.master.winfo_screenheight()  # This is the height of the screen
        # make my screen dimensions work
        w = 200  # The value of the width
        h = 200  # The value of the height of the window
        # calculate position x, y
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        # This is responsible for setting the dimensions of the screen and where it is placed
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.label = Label(self.master, text="label")
        self.Lb1 = Listbox(self.master, selectmode=MULTIPLE, height=3)
        self.label.pack()

        self.Lb1.insert(1, "Python")
        self.Lb1.insert(2, "Perl")
        self.Lb1.insert(3, "C")
        self.Lb1.bind('<<ListboxSelect>>', self.onselect)
        self.Lb1.pack()
        # self.Lb1.select_set(0) # sets the first element
        self.Lb1.select_set(0, END)

        button = Button(self.master, text="click", command=self.callback_click)
        button.pack()

        self.e = Entry(self.master, width=5)
        self.e.pack()
        self.e.delete(0, END)
        self.e.insert(0, "25")

        self.var = IntVar()
        self.c = Checkbutton(
            self.master,
            text="Kisallat",
            variable=self.var,
            command=self.cb)
        self.c.select()
        self.c.pack()

    def save_file(self):
        with open("Output.txt", "w") as text_file:
            text_file.write("Purchase Amount: {0}\n".format(123345))

    def cb(self):
        print("variable is " + str(self.var.get()))

    def onselect(self, evt):
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        print('You selected item %d: "%s"' % (index, value))

    def show_dist(self):
        geolocator = Nominatim()
        location = geolocator.geocode("Budapest, XXIII. Kerület Majosháza utca")
        location2 = geolocator.geocode("Holló utca Budapest, VII. Kerület ")
        print(location.address)
        loc1 = (location.latitude, location.longitude)
        loc2 = (location2.latitude, location2.longitude)
        print(vincenty(loc1, loc2).meters)
        return location.address

    def callback_click(self):
        self.label.configure(text="click")
        _values = [self.Lb1.get(idx) for idx in self.Lb1.curselection()]
        _message = ', '.join(_values)

        # self.show_message(alberlet.get_max_page_number())
        self.show_message(self.show_dist())

    def show_message(self, message):
        _messageWindow = Tk()
        _msg = Message(_messageWindow, text=message, width=200)
        _button = Button(_messageWindow, text='Ok', command=_messageWindow.destroy)
        _msg.pack()
        _button.pack()
        _messageWindow.mainloop()


if __name__ == '__main__':
    alberlet.get_page_urls()
    root = Tk()
    gui = Gui(master=root)
    gui.mainloop()

