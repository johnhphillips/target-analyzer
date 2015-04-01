from Tkinter import *
import tkMessageBox
import tkFileDialog

def stopProg(e):
    top.destroy()
    
def asksaveasfilename(self):
    filename = tkFileDialog.asksaveasfilename()
    
def openfilename():
    filename = tkFileDialog.askopenfilename(filetypes = (("All files", "*.*")
                                                         ,("XML files", "*.XML")))
    C.delete(1.0, END)
    C.insert(END, filename)
    
    
        
def error(errorCode):
    tkMessageBox.showerror("Format Error", "True Longitude for target is formatted incorrectly.\nExpected Format: XXX'XX.XXX\nCurrent Format: \nTarget not added\n\nPress OK to continue.")
    
top=Tk()
top.title("Contact Analysis Tool")
top.minsize(500, 250)
img = PhotoImage(file='default.gif')
top.tk.call('wm', 'iconphoto', top._w, img)


B = Button(top, text="Select Ground Truth XML File", command = openfilename)
B.grid(row=0, column=0, padx=10, pady=10)

C = Text(top, height=1, width=100)
C.grid(row=0, column=1, padx=10, pady=10)
C.insert(END, "No file selected")

A = Button(top, text="Select Mission XML File", command = openfilename)
A.grid(row=1, column=0, padx=10, pady=10)

D = Text(top, height=1, width=100)
D.grid(row=1, column=1, padx=10, pady=10)
D.insert(END, "No file selected")

top.mainloop()