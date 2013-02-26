#!/usr/bin/python

import pygtk
pygtk.require('2.0')
import gtk
from collections import deque

class Base:
  def destroy(self, widget, data=None):
    #this is where you put stuff
    print "Thanks for playing!"
    gtk.main_quit()

  def handleRegButton(self,widget):
    if widget.get_label().split('\n')[0] == "0":
      widget.set_label("1\n" + widget.get_label().split('\n')[1])
    else:
      widget.set_label("0\n" + widget.get_label().split('\n')[1])

  def dumpRegister(self,widget):
    for obj in self.buttonBox:
      temp = obj.get_label().split('\n')
      obj.set_label(temp[0] + "\n" + temp[0])

  def __init__(self):
    # setup display deque
    maxPoints = 50
    self.data = deque([0,0,0,0,0],maxPoints)
    
    # setup window
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.window.set_position(gtk.WIN_POS_CENTER)
    self.window.set_size_request(500,200)
    self.window.set_title("Pocasa - Pi")
    self.window.connect("destroy", self.destroy)

    # main vertical layout
    self.mainBox = gtk.VBox()

    # hlayout for register buttons
    self.buttonBox = gtk.HBox()

    # 16 registers
    for i in range(16):
      button = gtk.Button("0\n0")
      button.set_name("reg_"+str(i))
      button.connect("clicked",self.handleRegButton)
      self.buttonBox.pack_start(button)
    # add buttons to main layout 
    self.mainBox.pack_start(self.buttonBox)
    
    # options layout
    self.optionBox = gtk.HBox()
    self.btnDump = gtk.Button("Dump")
    self.btnDump.connect("clicked", self.dumpRegister)
    self.optionBox.pack_start(self.btnDump)
    self.mainBox.pack_start(self.optionBox)

    # add main layout to the window
    self.window.add(self.mainBox)

    self.window.show_all()

  def main(self):
    gtk.main()

if __name__ == "__main__":
  base = Base()
  base.main()
