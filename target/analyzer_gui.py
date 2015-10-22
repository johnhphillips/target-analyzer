# target-analyzer gui front-end for analyzer functions
# Copyright (C) 2015 John Phillips, SPAWAR Systems Center Pacific
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from Tkinter import *

import tkMessageBox
import tkFileDialog

from subprocess import Popen
import analyzer

# TODO: Implement error checking / dialogs / prompts

# max threshold distance between target and ground truth to state they are the same (m) (default of 40 m)
max_dist = 40

ground_truth = ''
input_file = ''
output_file = ''

def stopProg(e):
    top.destroy()
    
def _set_maxdist(name):
    global max_dist
    max_dist = name
    
def _get_maxdist():
    return max_dist

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
    # get threshold value from text box
    threshold = float(threshold.get("1.0", 'end-1c'))
    _set_maxdist(threshold)
    
    # build ground truth list from input XML file
    list_one = analyzer.contact_parser(ground_truth)

    # build contact list from contact XML file
    list_two = analyzer.contact_parser(input_file)
    analyzer.contact_localization(list_one, list_two, _get_maxdist(), _get_outputfile())
    p = Popen(_get_outputfile(), shell=True)

def open_groundtruth():
    filename = tkFileDialog.askopenfilename(filetypes = (("All files", "*.*")
                                                         ,("MEDAL files", "*.XML")))
    if len(filename) > 0:
        _set_groundtruth(filename)
        filename = filename.split('/')
        filename = filename[len(filename) - 1]
#         B.delete(1.0, END)
#         B.insert(END, filename)
        open_groundtruth_text.set(filename)
    
def open_contacts():
    filename = tkFileDialog.askopenfilename(filetypes = (("All files", "*.*")
                                                         ,("MEDAL files", "*.XML")))
    if len(filename) > 0:
        _set_inputfile(filename)
        filename = filename.split('/')
        filename = filename[len(filename) - 1]
#         D.delete(1.0, END)
#         D.insert(END, filename)
        open_filename_text.set(filename)
    
def save_filename():
    filename = tkFileDialog.asksaveasfilename(filetypes = (("All files", "*.*")
                                                           ,("CSV files", "*.CSV")), defaultextension = ".csv")
    
    if len(filename) > 0:
        _set_outputfile(filename)
        filename = filename.split('/')
        filename = filename[len(filename) - 1]
#         F.delete(1.0, END)
#         F.insert(END, filename)
        save_filename_text.set(filename)
        
def add_box():
    current_row = len(all_contacts)
    f_2_x = Frame(f_2, bg = "blue")
    f_2_x.grid(row=current_row, column=0)
    
    X = Button(f_2_x, text="Contact MEDAL File", height=1, width=20, command = open_contacts)
    X.grid(row=0, column=0, padx=10, pady=10)
    
    Y = StringVar()
    Label(f_2_x, textvariable = Y, relief=GROOVE, height=1, width=20).grid(row=0, column=1, padx=10, pady=10)
    Y.set("No file selected")
    
    # add current contact frame to contact list
    all_contacts.append(f_2_0)
    
def error(errorCode):
    tkMessageBox.showerror("Format Error", "True Longitude for target is formatted incorrectly.\nExpected Format: XXX'XX.XXX\nCurrent Format: \nTarget not added\n\nPress OK to continue.")
    
all_contacts = []

top=Tk()
top.title("Contact Analysis Tool")
top.minsize(250, 100)

top.iconbitmap('default.ico')

f_1 = Frame(top)
f_1.grid(row=0, column=0)

f_2 = Frame(top)
f_2.grid(row=1, column=0)

f_2_0 = Frame(f_2, bg = "red")
f_2_0.grid(row=0, column=0)

f_3 = Frame(top)
f_3.grid(row=2, column=0)

open_groundtruth_button = Button(f_1, text="Ground Truth MEDAL File", height=1, width=20, command = open_groundtruth)
open_groundtruth_button.grid(row=0, column=0, padx=10, pady=10)

open_groundtruth_text = StringVar()
Label(f_1, textvariable = open_groundtruth_text, relief=GROOVE, height=1, width=20).grid(row=0, column=1, padx=10, pady=10)
open_groundtruth_text.set("No file selected")

open_file_button = Button(f_2_0, text="Contact MEDAL File", height=1, width=20, command = open_contacts)
open_file_button.grid(row=0, column=0, padx=10, pady=10)

open_filename_text = StringVar()
Label(f_2_0, textvariable = open_filename_text, relief=GROOVE, height=1, width=20).grid(row=0, column=1, padx=10, pady=10)
open_filename_text.set("No file selected")


# add current contact frame to contact list
all_contacts.append(f_2_0)

save_file_button = Button(f_3, text="Save As", height=1, width=20, command = save_filename)
save_file_button.grid(row=0, column=0, padx=10, pady=10)

save_filename_text = StringVar()
Label(f_3, textvariable = save_filename_text, relief=GROOVE, height=1, width=20).grid(row=0, column=1, padx=10, pady=10)
save_filename_text.set("No file selected")

analyze_button = Button(f_3, text="Analyze", height=1, width=20, command=analyze_files)
analyze_button.grid(row=1, column=0, padx=10, pady=10)

add_file_button = Button(f_3, text="Add Contact MEDAL File", height=1, width=20, command=add_box)
add_file_button.grid(row=1, column=1, padx=10, pady=10)

threshold_label = Label(f_3, text="Match Threshold (m)")
threshold_label.grid(row=2, column=0, padx=10, pady=10)

threshold = Text(f_3, height=1, width=18)
threshold.grid(row=2, column=1, padx=10, pady=10)
threshold.insert(END, max_dist)

top.mainloop()