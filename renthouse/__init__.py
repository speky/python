#!/usr/bin/python

__author__ = 'speky'
import alberlet
import Tkinter

window = Tkinter.Tk()

label = Tkinter.Label(window, text="label")
Lb1 = Tkinter.Listbox(window, selectmode=Tkinter.MULTIPLE, height=3)

def init_window():
    window.title("Awsome kereso")
    #window.geometry("500x500")
    label.pack()

    Lb1.insert(1, "Python")
    Lb1.insert(2, "Perl")
    Lb1.insert(3, "C")
    Lb1.bind('<<ListboxSelect>>', onselect)
    Lb1.pack()

    button = Tkinter.Button(window, text="click", command=callback_click)
    button.pack()

def onselect(evt):
    # Note here that Tkinter passes an event object to onselect()
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    print 'You selected item %d: "%s"' % (index, value)

def callback_click():
    label.configure(text="click")
    _values = [Lb1.get(idx) for idx in Lb1.curselection()]
    _message = ', '.join(_values)
    show_message(_message)


def show_message(message):
    _messageWindow = Tkinter.Tk()
    _msg = Tkinter.Message(_messageWindow, text = message, width = 200)
    _button = Tkinter.Button(_messageWindow, text='Ok', command = _messageWindow.destroy)
    _msg.pack()
    _button.pack()
    _messageWindow.mainloop()

init_window()


window.mainloop()
