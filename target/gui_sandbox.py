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

#------------------------------------

def addBox():
    print "ADD"

    ent = Entry(root)
    ent.pack()

    all_entries.append( ent )

#------------------------------------

def showEntries():

    for number, ent in enumerate(all_entries):
        print number, ent.get()

#------------------------------------

all_entries = []

root = Tk()

showButton = Button(root, text='Show all text', command=showEntries)
showButton.pack()

addboxButton = Button(root, text='<Add Time Input>', fg="Red", command=addBox)
addboxButton.pack()

root.mainloop()

#------------------------------------