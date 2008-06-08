#!/usr/bin/env python
#
# GPytage leftpanel.py module
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
from datastore import E_NAME, E_DATA, E_EDITABLE, E_PARENT, E_MODIFIED
import rightpanel
from panelfunctions import switchListView

leftview = gtk.TreeView(datastore.datastore) #create the container

leftview.set_search_column(E_NAME)
#columns
namecol = gtk.TreeViewColumn('Package File')
testcol = gtk.TreeViewColumn('Flags')
boolcol = gtk.TreeViewColumn() #editable col
filecol = gtk.TreeViewColumn()
#add to tree
leftview.append_column(namecol)
leftview.append_column(testcol)
leftview.append_column(boolcol)
leftview.append_column(filecol)

#render cell
cell = gtk.CellRendererText()
cell1 = gtk.CellRendererText()

#add cols to cell
namecol.pack_start(cell, True)
namecol.set_attributes(cell, text=E_NAME)
namecol.add_attribute(cell, "editable", E_EDITABLE)#set row editable
namecol.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)

boolcol.set_visible(False)
filecol.set_visible(False)

testcol.pack_start(cell1, True)
testcol.set_attributes(cell1, text=1)
testcol.add_attribute(cell1, "editable", E_EDITABLE)#set row editable
testcol.set_expand(True)
testcol.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
testcol.set_visible(False)

###########Scroll Window#########################
scroll = gtk.ScrolledWindow()
scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
scroll.add_with_viewport(leftview)

############Drag and Drop####################
#note: is DND even needed for left panel?
leftview.enable_model_drag_dest([('text/plain', 0, 0)], gtk.gdk.ACTION_DEFAULT)
import panelfunctions
leftview.connect("drag_data_received", panelfunctions.get_dragdestdata)
leftview.connect("drag-motion", switchListView)

###########some variables####################
last_parent = None

def _clicked(treeview, *args):
	""" Handle treeview clicks """
	global last_parent
	model, iter = treeview.get_selection().get_selected()
	if iter: parent = model.get_value(iter,E_PARENT).strip('*')
	else: parent = last_parent.strip('*')
	# has the selection really changed?
	if parent.strip('*') != last_parent:
		print("LEFTPANEL: parent change detected")
		list = model.get_value(iter, E_NAME).strip('*')
		print list
		print parent
		if parent.strip('*') == 'package.' + list:
			rightpanel.setListModel(parent.strip('*'))
		else:
			rightpanel.setListModel(list.strip('*'))
	else: #fixes bug: if two subfiles are selected after each other with same parent
		list = model.get_value(iter, E_NAME).strip('*')
		rightpanel.setListModel(list)
	# save current selection as last selected
	last_parent = parent.strip('*')

#Signals
leftview.connect("cursor-changed", _clicked)