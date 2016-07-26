# target-analyzer analyzer_gui 
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

class Main_Application(tk.Frame):
    # Initialize main window
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        self._max_input = 10
        self._filename_default = 'No file selected'
        
        self._threshold = 40
        
        self._contact_frames = []
        self._ground_truth = self._filename_default
        self._save_filename = self._filename_default
        
        # Build top frame
        self.top_frame = tk.Frame(self.parent)
        self.top_frame.grid(row=0, column=0)
        
        # Populate top frame
        self.open_groundtruth_button = tk.Button(self.top_frame, text="Ground Truth MEDAL File", height=1, width=20, command = self.open_filename)
        self.open_groundtruth_button.grid(row=0, column=0, padx=10, pady=10)

        self.open_groundtruth_text = tk.StringVar()
        tk.Label(self.top_frame, textvariable = self.open_groundtruth_text, relief=tk.GROOVE, height=1, width=20).grid(row=0, column=1, padx=10, pady=10)
        self.open_groundtruth_text.set(self._ground_truth)
        
        # Build middle frame / first inner frame
        self.middle_frame = tk.Frame(self.parent)
        self.middle_frame.grid(row=1, column=0)

        # Build first inner frame and populate
        self.new_contact_frame()
            
        self.bottom_frame = tk.Frame(self.parent)
        self.bottom_frame.grid(row=2, column=0)
        
        # Populate the bottom frame
        self.save_file_button = tk.Button(self.bottom_frame, text="Save As", height=1, width=20, command = self.save_filename)
        self.save_file_button.grid(row=0, column=0, padx=10, pady=10)

        self.save_filename_text = tk.StringVar()
        tk.Label(self.bottom_frame, textvariable = self.save_filename_text, relief=tk.GROOVE, height=1, width=20).grid(row=0, column=1, padx=10, pady=10)
        self.save_filename_text.set(self._save_filename)

        self.analyze_button = tk.Button(self.bottom_frame, text="Analyze", height=1, width=20, command=self.analyze_files)
        self.analyze_button.grid(row=1, column=0, padx=10, pady=10)

        self.add_file_button = tk.Button(self.bottom_frame, text="Add Contact MEDAL File", height=1, width=20, command=self.new_contact_frame)
        self.add_file_button.grid(row=1, column=1, padx=10, pady=10)

        threshold_label = tk.Label(self.bottom_frame, text="Match Threshold (m)")
        threshold_label.grid(row=2, column=0, padx=10, pady=10)

        self.threshold = tk.Text(self.bottom_frame, height=1, width=18)
        self.threshold.grid(row=2, column=1, padx=10, pady=10)
        self.threshold.insert(tk.END, self._threshold)
        
    def open_filename(self):
        filename = tkFileDialog.askopenfilename(filetypes = (("All files", "*.*")
                                                         ,("MEDAL files", "*.XML")))
    
        if len(filename) > 0:
            self._ground_truth = filename
            filename = filename.split('/')
            filename = filename[len(filename) - 1]
            if len(filename) > 20:
                filename = filename[:20] + "..."
            self.open_groundtruth_text.set(filename)
            
        
    def new_contact_frame(self):
        if len(self._contact_frames) < self._max_input:
            self.frame = Contact_Frame(self)
            # Add to list of inner frames
            self._contact_frames.append(self.frame)
        else:
            self.error(2)
        
    def save_filename(self):
        
        filename = tkFileDialog.asksaveasfilename(filetypes = (("All files", "*.*")
                                                           ,("CSV files", "*.csv")), defaultextension = ".csv")
        if len(filename) > 0:
            self._save_filename = filename
            filename = filename.split('/')
            filename = filename[len(filename) - 1]
            if len(filename) > 20:
                filename = filename[:20] + "..."
            self.save_filename_text.set(filename)
            
    def analyze_files(self):
        # get threshold value from text box
        threshold = float(self.threshold.get("1.0", 'end-1c'))
        _threshold = threshold
        
        if self._ground_truth == self._filename_default or self._save_filename == self._filename_default or self._contact_frames[0]._filename == self._filename_default:
            self.error(3)
            return
    
        else:
            # build ground truth list from input XML file
            list_one = analyzer.contact_parser(self._ground_truth)
            
            # empty list to hold all contacts 
            list_two = []
            
            
            
            # case where only one input file is used
            if len(self._contact_frames) == 1:         
                # build contact list from contact XML file
                list_two = analyzer.contact_parser(self._contact_frames[0]._filename)
#                 analyzer._print_contacts(list_one)
#                 print "---"
#                 analyzer._print_contacts(list_two)
                analyzer.contact_localization(list_one, list_two, self._threshold, self._save_filename)
                Popen(self._save_filename, shell=True)
                
            elif len(self._contact_frames) > 1:
                # read individual contact XML files and product output            
                for frames in self._contact_frames:
                    # if 'No file selected' skip
                    if frames._filename == self._filename_default:
                        continue
                    current_filename = frames._filename.split('.')
                    current_filename = current_filename[0] + '.csv'

                    # build contact list from contact XML file
                    current_list = analyzer.contact_parser(frames._filename)
                        # add new to list two
                    for contacts in current_list:
                        list_two.append(contacts)
                    
                    analyzer.contact_localization(list_one, current_list, self._threshold, current_filename)
                    Popen(current_filename, shell=True)
                
                # if more than one file create summary file
                if len(self._contact_frames) > 1:   
                    analyzer.contact_localization(list_one, list_two, self._threshold, self._save_filename)
                    Popen(self._save_filename, shell=True)
            
    def error(self, error_code):
        if error_code == 2:
            tkMessageBox.showerror("Input File Error", "Maximum number of input files (" + str(self._max_input) + ") reached.\n\n\nPress OK to continue.")
        if error_code == 3:
            tkMessageBox.showerror("File Error", "I/O file name not selected.\n\n\nPress OK to continue.")
        
class Contact_Frame:
    def __init__(self, parent):
        self.parent = parent
        
        self.current_row = len(parent._contact_frames)
        self._filename = parent._filename_default
        
        self.middle_frame_0 = tk.Frame(parent.middle_frame)
        self.middle_frame_0.grid(row=self.current_row, column=0)
            
        open_file_button = tk.Button(self.middle_frame_0, text="Contact MEDAL File", height=1, width=20, command = self._set_filename)
        open_file_button.grid(row=0, column=0, padx=10, pady=10)

        self.open_filename_text = tk.StringVar()
        tk.Label(self.middle_frame_0, textvariable = self.open_filename_text, relief=tk.GROOVE, height=1, width=20).grid(row=0, column=1, padx=10, pady=10)
        # set file name to default
        self.open_filename_text.set(self._filename)
        
    def _set_filename(self):
        filename = tkFileDialog.askopenfilename(filetypes = (("All files", "*.*")
                                                         ,("MEDAL files", "*.XML")))
    
        if len(filename) > 0:
            self._filename = filename
            filename = filename.split('/')
            filename = filename[len(filename) - 1]
            if len(filename) > 20:
                filename = filename[:20] + "..."
            self.open_filename_text.set(filename)
            
        
def main(): 
    top = tk.Tk()
    top.title("Contact Analysis Tool v1.0 b5") #2016 07 25
    top.minsize(250, 100)
    top.iconbitmap('default.ico')
    Main_Application(top)
    top.mainloop()

if __name__ == '__main__':
    main()