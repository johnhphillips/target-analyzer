from Tkinter import *
import tkMessageBox
import tkFileDialog

def stopProg(e):
    top.destroy()
    
def asksaveasfilename(self):
    filename = tkFileDialog.asksaveasfilename()
    
def openfilename():
    filename = tkFileDialog.askopenfilename(filetypes = (("All files", "*.*")
                                                         ,("XLSX files", "*.xlsx")))
    print filename
    
        
def error(errorCode):
    tkMessageBox.showerror("Format Error", "True Longitude for target is formatted incorrectly.\nExpected Format: XXX'XX.XXX\nCurrent Format: \nTarget not added\n\nPress OK to continue.")
    
top=Tk()
top.title("Operator Contact Analysis Tool")
top.minsize(500, 250)
img = PhotoImage(file='default.gif')
top.tk.call('wm', 'iconphoto', top._w, img)

B = Button(top, text="Select Ground Truth PMD Report", command = openfilename)
B.grid(row=0, column=0, padx=10, pady=10)

A = Button(top, text="Select Operator PMD Report", command = openfilename)
A.grid(row=1, column=0, padx=10, pady=10)

top.mainloop()