#!/usr/bin/python

# Originally Created by Ryan Hatfield
# http://tophathacker.com
# tophathacker@gmail.com


# for setting bit: i |= 1 << b where b is the bit position
# for zeroing bit: i &= ~(1<<b) where b is teh bit position

import pygtk
pygtk.require('2.0')
import gtk

# this is obviously the wrong way to do this, but i'll fix it later
import sys
sys.path.insert(0,'../shiftModule/build/lib.linux-armv6l-2.7')
try:
  import shift
except:
  print "build shiftModule first with\npython setup.py build\nfrom the shiftModule directory"
  sys.exit()

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
      tempNumb = obj.get_label().split('\n')
      obj.set_label(tempNumb[0] + "\n" + tempNumb[0])
      tempName = obj.get_name().split('_')
      if tempNumb[0] == "1":
        self.register |= 1 << int(tempName[1])
      else:
        self.register &= ~(1<<int(tempName[1]))
    shift.shift_out(self.register)

  def __init__(self):
    # setup display deque
    maxPoints = 50
    self.data = deque([0,0,0,0,0],maxPoints)
    
		# register variable
    self.register = 0

		# setup pins for shift module
    shift.setup_pins()

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
