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

        self.master = master
        self.init_window()


    def add_portal_list(self):
        self.labelSearch = Label(self.master, text="Oldalak ahol keres")
        self.labelSearch.grid(row=0, column=0, columnspan=2)

        self.Lb1 = Listbox(self.master, selectmode=MULTIPLE, height=3)
        self.Lb1.insert(1, 'alberlet.hu')
        # self.Lb1.insert(2, "...")

        self.Lb1.bind('<<ListboxSelect>>', self.onselect)
        self.Lb1.grid(row=1, column=0, columnspan=2, rowspan=2)
        # select all
        self.Lb1.select_set(0, END)


    def add_price(self):
        self.label = Label(self.master, text="Ár (ezerFt)")
        self.label.grid(columnspan=2, row=0, column=2)

        self.entryPrice = Entry(self.master, width=5)
        self.entryPrice.grid(row=1, column=2)
        self.entryPrice.delete(0, END)
        self.entryPrice.insert(0, "0")

        self.entryPrice2 = Entry(self.master, width=5)
        self.entryPrice2.grid(row=1, column=3, padx=10)
        self.entryPrice2.delete(0, END)
        self.entryPrice2.insert(0, "60")


    def add_size(self):
        self.labelSize = Label(self.master, text="Méret (m^2)")
        self.labelSize.grid(columnspan=2,row=2, column=2)

        self.entrySize = Entry(self.master, width=5)
        self.entrySize.grid(row=3, column=2)
        self.entrySize.delete(0, END)
        self.entrySize.insert(0, "0")

        self.entrySize2 = Entry(self.master, width=5)
        self.entrySize2.grid(row=3, column=3, padx=10)
        self.entrySize2.delete(0, END)
        self.entrySize2.insert(0, "x")


    def add_checkboxes(self):
        self.dog = IntVar()
        self.dogCheckBox = Checkbutton(
            self.master,
            text="Kisállat",
            variable=self.dog)
        self.dogCheckBox.select()
        self.dogCheckBox.grid(row=5, column=2)

        self.furniture = IntVar()
        self.furnitureCheckBox = Checkbutton(
            self.master,
            text="Bútorozott",
            variable=self.furniture)
        self.furnitureCheckBox.select()
        self.furnitureCheckBox.grid(row=5, column=3)


    def add_found(self):
        self.labelFounds = Label(self.master, text="Találtaok:")
        self.labelFounds.grid(row=6, column=0, sticky=E)

        self.entryFounds = Entry(self.master, width=5)
        self.entryFounds.grid(row=6, column=1, sticky=W)
        self.entryFounds .delete(0, END)
        self.entryFounds .insert(0, "0")


    def add_district(self):
        self.labelDistrict = Label(self.master, text="Kerülets:")
        self.labelDistrict.grid(row=6, column=2, sticky=E)

        self.entryFounds = Entry(self.master, width=15)
        self.entryFounds.grid(row=6, column=3, sticky=W)
        self.entryFounds .delete(0, END)
        self.entryFounds .insert(0, "xiv+xvi")

    def init_window(self):
        self.master.title("Alberlet kereso")
        # get screen width and height
        ws = self.master.winfo_screenwidth()  # This value is the width of the screen
        hs = self.master.winfo_screenheight()  # This is the height of the screen
        # make my screen dimensions work
        w = 350  # The value of the width
        h = 360  # The value of the height of the window
        # calculate position x, y
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        # This is responsible for setting the dimensions of the screen and where it is placed
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.add_portal_list()
        self.add_price()
        self.add_size()
        self.add_checkboxes()
        self.add_found()
        self.add_district()

        button = Button(self.master, text="Keresés", command=self.callback_click)
        button.grid(row=5, column=0, columnspan=2)

        self.text = Text(self.master, width=40, height=10)
        self.text.grid(row=7, column=0, columnspan=5, rowspan=3, padx=5, pady=5)
        self.text.grid(row=7, column=0, columnspan=5, rowspan=3, padx=5, pady=5)
       #     self.text.insert(INSERT, "asdasdsdfg \n")


    def save_file(self):
        with open("Output.txt", "w") as text_file:
            text_file.write("Purchase Amount: {0}\n".format(123345))


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
        _values = [self.Lb1.get(idx) for idx in self.Lb1.curselection()]
        _message = ', '.join(_values)
        print(_values)
        # self.show_message(alberlet.get_max_page_number())
        #self.show_message(self.show_dist())

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
    root.resizable(width=FALSE, height=FALSE)
    gui = Gui(master=root)
    gui.mainloop()

