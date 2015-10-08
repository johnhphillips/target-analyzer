# target-analyzer gui_sandbox 
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

# #------------------------------------
# 
# def addBox():
#     print "ADD"
# 
#     frame = Frame(root)
#     frame.pack()
# 
#     Label(frame, text='From').grid(row=0, column=0)
# 
#     ent1 = Entry(frame)
#     ent1.grid(row=1, column=0)
# 
#     Label(frame, text='To').grid(row=0, column=1)
# 
#     ent2 = Entry(frame)
#     ent2.grid(row=1, column=1)
# 
#     all_entries.append( (ent1, ent2) )
# 
# #------------------------------------
# 
# def showEntries():
# 
#     for number, (ent1, ent2) in enumerate(all_entries):
#         print number, ent1.get(), ent2.get()
# 
# #------------------------------------
# 
# all_entries = []
# 
# root = Tk()
# 
# showButton = Button(root, text='Show all text', command=showEntries)
# showButton.pack()
# 
# addboxButton = Button(root, text='<Add Time Input>', fg="Red", command=addBox)
# addboxButton.pack()
# 
# root.mainloop()

from Tkinter import *

main = Tk()

def leftKey(event):
    print "Left key pressed"

def rightKey(event):
    print "Right key pressed"

frame = Frame(main, width=100, height=100)
main.bind('<Left>', leftKey)
main.bind('<Right>', rightKey)
frame.pack()
main.mainloop()