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

import Tkinter as tk

import tkMessageBox
import tkFileDialog

from subprocess import Popen
import analyzer
from target.analyzer import contact_localization

# TODO: Implement error checking / dialogs / prompts
MAX_INPUT = 10

# max threshold distance between target and ground truth to state they are the same (m) (default of 40 m)
max_dist = 40

filename_default = 'No file selected'

ground_truth = ''
input_files = ['']
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
    _threshold = float(threshold.get("1.0", 'end-1c'))
    _set_maxdist(_threshold)
    
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
    # check if number of inputs is less than max (10)
    if len(input_files) < MAX_INPUT:
        current_row = len(all_contacts)
        middle_frame_x = tk.Frame(middle_frame, bg = "blue")
        middle_frame_x.grid(row=current_row, column=0)
    
        X = tk.Button(middle_frame_x, text="Contact MEDAL File", height=1, width=20, command = lambda: print_row(current_row))
        X.grid(row=0, column=0, padx=10, pady=10)
    
        Y = tk.StringVar()
        tk.Label(middle_frame_x, textvariable = Y, relief=tk.GROOVE, height=1, width=20).grid(row=0, column=1, padx=10, pady=10)
        # set file name to default
        input_files.append(filename_default)
        Y.set(filename_default)
        
        # add current contact frame to contact list
        all_contacts.append(middle_frame_x)
       
    else:
        error(2)
        
def print_row(row):
    print row
    
def error(error_code):
    if error_code == 1:
        tkMessageBox.showerror("Format Error", "True Longitude for target is formatted incorrectly.\nExpected Format: XXX'XX.XXX\nCurrent Format: \nTarget not added\n\nPress OK to continue.")
    if error_code == 2:
        tkMessageBox.showerror("Input File Error", "Maximum number of input files (10) reached.\n\n\nPress OK to continue.")


all_contacts = []

top=tk.Tk()
top.title("Contact Analysis Tool")
top.minsize(250, 100)

top.iconbitmap('default.ico')

top_frame = tk.Frame(top)
top_frame.grid(row=0, column=0)

middle_frame = tk.Frame(top)
middle_frame.grid(row=1, column=0)

middle_frame_0 = tk.Frame(middle_frame, bg = "red")
middle_frame_0.grid(row=0, column=0)

bottom_frame = tk.Frame(top)
bottom_frame.grid(row=2, column=0)

open_groundtruth_button = tk.Button(top_frame, text="Ground Truth MEDAL File", height=1, width=20, command = open_groundtruth)
open_groundtruth_button.grid(row=0, column=0, padx=10, pady=10)

open_groundtruth_text = tk.StringVar()
tk.Label(top_frame, textvariable = open_groundtruth_text, relief=tk.GROOVE, height=1, width=20).grid(row=0, column=1, padx=10, pady=10)
open_groundtruth_text.set(filename_default)

open_file_button = tk.Button(middle_frame_0, text="Contact MEDAL File", height=1, width=20, command = open_contacts)
open_file_button.grid(row=0, column=0, padx=10, pady=10)

open_filename_text = tk.StringVar()
tk.Label(middle_frame_0, textvariable = open_filename_text, relief=tk.GROOVE, height=1, width=20).grid(row=0, column=1, padx=10, pady=10)
# set file name to default
input_files[0] = filename_default
open_filename_text.set(filename_default)

# add current contact frame to contact list
all_contacts.append(middle_frame_0)

save_file_button = tk.Button(bottom_frame, text="Save As", height=1, width=20, command = save_filename)
save_file_button.grid(row=0, column=0, padx=10, pady=10)

save_filename_text = tk.StringVar()
tk.Label(bottom_frame, textvariable = save_filename_text, relief=tk.GROOVE, height=1, width=20).grid(row=0, column=1, padx=10, pady=10)
save_filename_text.set(filename_default)

analyze_button = tk.Button(bottom_frame, text="Analyze", height=1, width=20, command=analyze_files)
analyze_button.grid(row=1, column=0, padx=10, pady=10)

add_file_button = tk.Button(bottom_frame, text="Add Contact MEDAL File", height=1, width=20, command=add_box)
add_file_button.grid(row=1, column=1, padx=10, pady=10)

threshold_label = tk.Label(bottom_frame, text="Match Threshold (m)")
threshold_label.grid(row=2, column=0, padx=10, pady=10)

threshold = tk.Text(bottom_frame, height=1, width=18)
threshold.grid(row=2, column=1, padx=10, pady=10)
threshold.insert(tk.END, max_dist)

top.mainloop()