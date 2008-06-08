#!/usr/bin/env python
#
# GPytage rightpanel.py module
#
############################################################################
#    Copyright (C) 2008 by Kenneth Prugh                                   #
#    ken69267@gmail.com                                                    #
#                                                                          #
#    This program is free software; you can redistribute it and#or modify  #
#    it under the terms of the GNU General Public License as published by  #
#    the Free Software Foundation under version 2 of the license.          #
#                                                                          #
#    This program is distributed in the hope that it will be useful,       #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#    GNU General Public License for more details.                          #
#                                                                          #
#    You should have received a copy of the GNU General Public License     #
#    along with this program; if not, write to the                         #
#    Free Software Foundation, Inc.,                                       #
#    59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
############################################################################

import pygtk; pygtk.require("2.0")
import gtk
import datastore
from datastore import E_NAME, E_DATA, E_EDITABLE, E_PARENT, E_MODIFIED, new_entry
from window import title
from panelfunctions import mselected, fileEdited

rightview = gtk.TreeView()
rightselection = rightview.get_selection()

#set MULTIPLE selection mode
rightselection.set_mode(gtk.SELECTION_MULTIPLE)

def setListModel(list): #we need to switch the model on click
	try:
		rightview.set_model()
		rightview.set_model(datastore.lists[list]) #example
		namecol.queue_resize()
		testcol.queue_resize()
		filecol.queue_resize()
	except:
		print 'RIGHTPANEL: setListModel(); failed'
		return

rightview.set_search_column(E_NAME)
#columns
namecol = gtk.TreeViewColumn('Value')
testcol = gtk.TreeViewColumn('Flags')
boolcol = gtk.TreeViewColumn() #editable col
filecol = gtk.TreeViewColumn()
#add to tree
rightview.append_column(namecol)
rightview.append_column(testcol)
rightview.append_column(boolcol)
rightview.append_column(filecol)
#render cell
cell = gtk.CellRendererText()
cell1 = gtk.CellRendererText()

#add cols to cell
namecol.pack_start(cell, True)
namecol.set_attributes(cell, text=E_NAME)
namecol.add_attribute(cell, "editable", E_EDITABLE)#set row editable
namecol.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)

testcol.pack_start(cell1, True)
testcol.set_attributes(cell1, text=E_DATA)
testcol.add_attribute(cell1, "editable", E_EDITABLE)#set row editable
testcol.set_expand(True)
testcol.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)

boolcol.set_visible(False)
filecol.set_visible(False)

###########Scroll Window#########################
scroll = gtk.ScrolledWindow()
scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
scroll.add_with_viewport(rightview)

############Drag and Drop####################
rightview.set_reorderable(True) # allow inline drag and drop
rightview.enable_model_drag_source(gtk.gdk.BUTTON1_MASK, [('text/plain', 0, 0)], gtk.gdk.ACTION_DEFAULT | gtk.gdk.ACTION_MOVE)
rightview.enable_model_drag_dest([('text/plain', 0, 0)], gtk.gdk.ACTION_DEFAULT)
import panelfunctions
rightview.connect("drag_begin", panelfunctions.drag_begin_signal)
rightview.connect("drag_data_delete", panelfunctions.drag_data_delete_signal)
rightview.connect("drag_data_received", panelfunctions.get_dragdestdata)

#Callbacks
def edited_cb(cell, path, new_text, col):
	""" Indicate file has been edited """
	model = rightview.get_model()
	model[path][col] = new_text
	model[path][E_MODIFIED] = True
	#Indicate file status
	fileEdited() #edit rightpanel to show status
	title("* GPytage")
	return

def insertrow(arg):
	""" Insert row below selected row(s) """
	treeview = rightview
	model, iterdict = mselected(treeview)
	for iter,value in iterdict.iteritems(): #Should only have 1 via right click.. funky results with accelerator.
		if value == True:
			parent = model.get_value(iter, E_PARENT)
			new = model.insert_after(iter, new_entry(parent=parent))
			path = model.get_path(new)
			treeview.set_cursor_on_cell(path, namecol, cell, True)
			title("* GPytage")

def deleterow(arg):
	""" Delete selected row(s) """
	treeview = rightview
	model, iterdict = mselected(treeview)
	for iter,value in iterdict.iteritems():
		if value == True:
			model.remove(iter)
			fileEdited()
			title("* GPytage")

def commentRow(window):
	""" Comment selected row(s) """
	treeview = rightview
	model, iterdict = mselected(treeview)
	for iter,value in iterdict.iteritems():
		if value == True:
			old = model.get_value(iter, E_NAME)
			if old.startswith("#") is False:
				model.set_value(iter, E_NAME, "#"+old)
				fileEdited()
				title("* GPytage")

def uncommentRow(window):
	""" Uncomment selected row(s) """
	treeview = rightview
	model, iterdict = mselected(treeview)
	for iter,value in iterdict.iteritems():
		if value == True:
			old = model.get_value(iter, E_NAME)
			if old.startswith("#"):
				model.set_value(iter, E_NAME, old[1:])
				fileEdited()
				title("* GPytage")

def clicked(view, event):#needs updating from dual panels
	""" Right click menu for rightview """
	if event.button == 3:
		menu = gtk.Menu()
		irow = gtk.MenuItem("Insert Package")
		irow.connect("activate", insertrow)
		drow = gtk.MenuItem("Delete Package")
		drow.connect("activate", deleterow)
		menu.append(irow)
		menu.append(drow)
		menu.show_all()
		menu.popup(None, None, None, event.button, event.time)

#Signals
cell.connect("edited", edited_cb, E_NAME)
cell1.connect("edited", edited_cb, E_DATA)
rightview.connect("button_press_event", clicked)