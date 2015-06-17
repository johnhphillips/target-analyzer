from Tkinter import *

import tkMessageBox
import tkFileDialog

from subprocess import Popen

import formatter

# max threshold distance between target and ground truth to state they are the same (m)
MAX_DIST = 40

ground_truth = ''
input_file = ''
output_file = ''

def stopProg(e):
    top.destroy()
    
def _set_groundtruth(name):
    global ground_truth
    ground_truth = name
    
def _get_groundtruth():
    return ground_truth

def _set_inputfile(name):
    global input_file
    input_file = name
    
def _get_inputfile():
    return input_file

def _set_outputfile(name):
    global output_file
    output_file = name
    
def _get_outputfile():
    return output_file
        
def analyze_files():
    # build ground truth list from input XML file
    list_one = formatter.contact_parser(ground_truth)

    # build contact list from contact XML file
    list_two = formatter.contact_parser(input_file)
    formatter.contact_localization(list_one, list_two, MAX_DIST, output_file)
    p = Popen(output_file, shell=True)

def open_groundtruth():
    filename = tkFileDialog.askopenfilename(filetypes = (("All files", "*.*")
                                                         ,("XML files", "*.XML")))
    if len(filename) > 0:
        filename = filename.split('/')
        filename = filename[len(filename) - 1]
        B.delete(1.0, END)
        B.insert(END, filename)
        _set_groundtruth(filename)
    
def open_contacts():
    filename = tkFileDialog.askopenfilename(filetypes = (("All files", "*.*")
                                                         ,("XML files", "*.XML")))
    if len(filename) > 0:
        filename = filename.split('/')
        filename = filename[len(filename) - 1]
        D.delete(1.0, END)
        D.insert(END, filename)
        _set_inputfile(filename) 
    
def save_filename():
    filename = tkFileDialog.asksaveasfilename(filetypes = (("All files", "*.*")
                                                           ,("CSV files", "*.CSV")), defaultextension = ".csv")
    
    if len(filename) > 0:
        filename = filename.split('/')
        filename = filename[len(filename) - 1]
        F.delete(1.0, END)
        F.insert(END, filename)
        _set_outputfile(filename)
    
def error(errorCode):
    tkMessageBox.showerror("Format Error", "True Longitude for target is formatted incorrectly.\nExpected Format: XXX'XX.XXX\nCurrent Format: \nTarget not added\n\nPress OK to continue.")
    
top=Tk()
top.title("Contact Analysis Tool")
top.minsize(250, 100)

img = Image("photo", file="default.gif")
top.tk.call('wm', 'iconphoto', top._w, img)


A = Button(top, text="Ground Truth XML File", height=1, width=20, command = open_groundtruth)
A.grid(row=0, column=0, padx=10, pady=10)

B = Text(top, height=1, width=20)
B.grid(row=0, column=1, padx=10, pady=10)
B.insert(END, "No file selected")

C = Button(top, text="Contact XML File", height=1, width=20, command = open_contacts)
C.grid(row=1, column=0, padx=10, pady=10)

D = Text(top, height=1, width=20)
D.grid(row=1, column=1, padx=10, pady=10)
D.insert(END, "No file selected")

E = Button(top, text="Save As", height=1, width=20, command = save_filename)
E.grid(row=2, column=0, padx=10, pady=10)

F = Text(top, height=1, width=20)
F.grid(row=2, column=1, padx=10, pady=10)
F.insert(END, "No file selected")

G = Button(top, text="Analyze", height=1, width=20, command = analyze_files)
G.grid(row=3, column=0, padx=10, pady=10)

top.mainloop()