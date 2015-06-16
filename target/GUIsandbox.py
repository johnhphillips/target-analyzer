from Tkinter import *
import tkMessageBox
import tkFileDialog

def stopProg(e):
    top.destroy()
        
def openGT():
    filename = tkFileDialog.askopenfilename(filetypes = (("All files", "*.*")
                                                         ,("XML files", "*.XML")))
    if len(filename) > 0:
        B.delete(1.0, END)
        B.insert(END, filename)
        filename = filename.split('/')
        print filename[len(filename) - 1]
    
def openMission():
    filename = tkFileDialog.askopenfilename(filetypes = (("All files", "*.*")
                                                         ,("XML files", "*.XML")))
    if len(filename) > 0:
        D.delete(1.0, END)
        D.insert(END, filename)
        filename = filename.split('/')
        print filename[len(filename) - 1] 
    
def asksaveasfilename():
    filename = tkFileDialog.asksaveasfilename(filetypes = (("All files", "*.*")
                                                           ,("CSV files", "*.CSV")), defaultextension = ".CSV")
    
    if len(filename) > 0:
        F.delete(1.0, END)
        F.insert(END, filename)
        filename = filename.split('/')
        print filename[len(filename) - 1]
    
def error(errorCode):
    tkMessageBox.showerror("Format Error", "True Longitude for target is formatted incorrectly.\nExpected Format: XXX'XX.XXX\nCurrent Format: \nTarget not added\n\nPress OK to continue.")
    
top=Tk()
top.title("Contact Analysis Tool")
top.minsize(500, 250)

img = Image("photo", file="default.gif")
top.tk.call('wm', 'iconphoto', top._w, img)


A = Button(top, text="Select Ground Truth XML File", command = openGT)
A.grid(row=0, column=0, padx=10, pady=10)

B = Text(top, height=1, width=100)
B.grid(row=0, column=1, padx=10, pady=10)
B.insert(END, "No file selected")

C = Button(top, text="Select Mission XML File", command = openMission)
C.grid(row=1, column=0, padx=10, pady=10)

D = Text(top, height=1, width=100)
D.grid(row=1, column=1, padx=10, pady=10)
D.insert(END, "No file selected")

E = Button(top, text="Select Output CSV File Name and Location", command = asksaveasfilename)
E.grid(row=2, column=0, padx=10, pady=10)

F = Text(top, height=1, width=100)
F.grid(row=2, column=1, padx=10, pady=10)
F.insert(END, "No file selected")

top.mainloop()