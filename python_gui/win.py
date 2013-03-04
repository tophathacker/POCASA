#!/usr/bin/python

# Originally Created by Ryan Hatfield
# http://tophathacker.com
# tophathacker@gmail.com


# for setting bit: i |= 1 << b where b is the bit position
# for zeroing bit: i &= ~(1<<b) where b is teh bit position

import pygtk
pygtk.require('2.0')
import gtk
import time
from threading import Thread
# this is obviously the wrong way to do this, but i'll fix it later
import sys
sys.path.insert(0,'../shiftModule/build/lib.linux-armv6l-2.7')
try:
  import shift
  shiftLoaded = True
except:
  print "build shiftModule first with\npython setup.py build\nfrom the shiftModule directory"
  #sys.exit()

from collections import deque
pointsX = deque([],10)
pointsY = deque([],10)

class getadc(Thread):
  def __init__(self,parent):
    self.parent = parent
    Thread.__init__(self)
    self.start()
  def run(self):
    self.wait = .5
    while 1:
      xy = shift.get_adc(self.parent.register)
      print xy
      #self.parent.testBox.set_text(str(xy[0]) + "," + str(xy[1])) 
#      self.parent.pointsX.append(xy[0])
#      self.parent.pointsY.append(xy[1])
      time.sleep(self.wait)

class Base:
  # Base class for the gui
  
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
    if self.shiftLoaded:
      self.register = shift.shift_out(self.register)
  
  def zeroDAC(self,widget):
    if self.shiftLoaded:
      self.register = shift.set_dac(self.register,0)
    self.setReg(self.register)

  def setReg(self,register):
    #print str(register)
    count = 0
    for obj in self.buttonBox:
      tempNumb = obj.get_label().split('\n')
      obj.set_label(tempNumb[0] + "\n" + str((register >> count) & 1))
      count+=1

  def setRegTest(self,widget):
    self.the_thread = getadc(self)

  def setDAC(self,widget):
    #if self.shiftLoaded:
    #  self.register = shift.set_dac(self.register, int(
    final = 0
    a = int(self.dacIntA.get_text())
    b = int(self.dacIntB.get_text())
    c = int(self.dacIntC.get_text())
    d = int(self.dacIntD.get_text())
    for i in range(7,-1,-1):
      if a >> i & 1:
        final |= 1 << (i + 24)
      else:
        final &= ~(1 << (i + 24))
    for i in range(7,-1,-1):
      if b >> i & 1:
        final |= 1 << (i + 16)
      else:
        final &= ~(1 << (i + 16))
    for i in range(7,-1,-1):
      if c >> i & 1:
        final |= 1 << (i + 8)
      else:
        final &= ~(1 << (i + 8))
    for i in range(7,-1,-1):
      if d >> i & 1:
        final |= 1 << i
      else:
        final &= ~(1 << i)
    #print str(bin(final))
    #print final
    if self.shiftLoaded:
      self.register = shift.set_dac(self.register,final)
    self.setReg(self.register)
    #self.set_dac(final)
 
  def set_dac(self,number):
    select = 6
    clock = 3
    data = 2
    
    self.register &= ~(1 << clock) # set clock low
    shift.shift_out(self.register)
    self.register &= ~(1 << select) # pull chip select low
    shift.shift_out(self.register)
   
    for i in range(31,-1,-1):
      if number >> i & 1:
        self.register |= 1 << data
        # print "set bit " + str(i) + " high \n"
      else:
        self.register &= ~(1 << data)
        # print "set bit " + str(i) + " low \n"
      shift.shift_out(self.register) #set data bit
      self.register |= 1 << clock # set clock high
      shift.shift_out(self.register)
      self.register &= ~(1 << clock) # set clock low again
      shift.shift_out(self.register)
    self.register |= 1 << select # set chip select high again
    self.register = shift.shift_out(self.register)
    

 
  def dacIntChanged(self,widget):
    hexer = "%x" % int(widget.get_text())
    biner = bin(int(widget.get_text()))[2:]
    name = widget.get_name()
    if name == "dacIntA":
      self.dacHexA.set_text(hexer)
      self.dacBinA.set_text(biner)
    elif name == "dacIntB":
      self.dacHexB.set_text(hexer)
      self.dacBinB.set_text(biner)
    elif name == "dacIntC":
      self.dacHexC.set_text(hexer)
      self.dacBinC.set_text(biner)
    elif name == "dacIntD":
      self.dacHexD.set_text(hexer)
      self.dacBinD.set_text(biner)

  def dacHexChanged(self,widget):
    inter = str(int(widget.get_text(), 16))
    biner = bin(int(widget.get_text(),16))[2:]
    name = widget.get_name()
    if name == "dacHexA":
      self.dacIntA.set_text(inter)
      self.dacBinA.set_text(biner)
    elif name == "dacHexB":
      self.dacIntB.set_text(inter)
      self.dacBinB.set_text(biner)
    elif name == "dacHexC":
      self.dacIntC.set_text(inter)
      self.dacBinC.set_text(biner)
    elif name == "dacHexD":
      self.dacIntD.set_text(inter)
      self.dacBinD.set_text(biner)

  def dacBinChanged(self,widget):
    inter = str(int(widget.get_text(),2))
    hexer = "%x" % int(inter)
    name = widget.get_name()
    if name == "dacBinA":
      self.dacIntA.set_text(inter)
      self.dacHexA.set_text(hexer)
    elif name == "dacBinB":
      self.dacIntB.set_text(inter)
      self.dacHexB.set_text(hexer)
    elif name == "dacBinC":
      self.dacIntC.set_text(inter)
      self.dacHexC.set_text(hexer)
    elif name == "dacBinD":
      self.dacIntD.set_text(inter)
      self.dacHexD.set_text(hexer)
  def mapInt(oldmin,oldmax,newmin,newmax,value):
    oldspan = oldmax - oldmin
    newspan = newmax - newmin

    valuescaled = float(value - oldmin) / float(oldspan)
    return newmin + (valuescaled * newspan)

  def area_expose_cb(self, area, event):
    self.style = self.area.get_style()
    self.gc = self.style.fg_gc[gtk.STATE_NORMAL]
    for i in range[0,len(self.pointsX)]:
      self.area.window.draw_line(self.gc, 0, 0, 100,100)
    return True 

  def __init__(self):
    # setup all gui stuff
    maxPoints = 50
    self.data = deque([0,0,0,0,0],maxPoints)
    
		# register variable
    self.register = 0

		# setup pins for shift module
    try:
      shift.setup_pins()
      self.shiftLoaded = True
    except:
      print "Shift library failed to load"
      self.shiftLoaded = False

    # setup window
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.window.set_position(gtk.WIN_POS_CENTER)
    self.window.set_size_request(900,400)
    self.window.set_title("Pocasa - Pi")
    self.window.connect("destroy", self.destroy)

    # main vertical layout
    self.mainBox = gtk.VBox()
    self.mainBox.set_border_width(10)

    # hlayout for register buttons
    self.buttonBox = gtk.HBox()

    # hlayout for register lables
    self.labelBox = gtk.HBox()

    # 16 registers
    for i in range(16):
      button = gtk.Button("0\n0")
      button.set_name("reg_"+str(i))
      button.connect("clicked",self.handleRegButton)
      self.buttonBox.pack_start(button)
      label = gtk.Label("Bit " + str(i))
      label.set_name("Bit_" + str(i))
      self.labelBox.pack_start(label)
    
    # make frame for shift
    frameShift = gtk.Frame("shift register")
    vbox = gtk.VBox()
    vbox.set_border_width(5)
    frameShift.add(vbox)

    # add labels to main layout then
    # add buttons to main layout 
    vbox.pack_start(self.labelBox)
    vbox.pack_start(self.buttonBox)
    self.btnDump = gtk.Button("Dump")
    self.btnDump.connect("clicked",self.dumpRegister)
    vbox.pack_start(self.btnDump)
    self.mainBox.pack_start(frameShift)
   
    self.dacIntBox = gtk.HBox()
    self.dacIntLabel = gtk.Label("Int")
    self.dacIntBox.pack_start(self.dacIntLabel,True,True,10)
    self.dacIntA = gtk.Entry(3)
    self.dacIntA.set_name("dacIntA")
    self.dacIntA.connect("changed",self.dacIntChanged)
    self.dacIntBox.pack_start(self.dacIntA,True,True,10)
    self.dacIntB = gtk.Entry(3)
    self.dacIntB.set_name("dacIntB")
    self.dacIntB.connect("changed",self.dacIntChanged)
    self.dacIntBox.pack_start(self.dacIntB,True,True,10)
    self.dacIntC = gtk.Entry(3)
    self.dacIntC.set_name("dacIntC")
    self.dacIntC.connect("changed",self.dacIntChanged)
    self.dacIntBox.pack_start(self.dacIntC,True,True,10)
    self.dacIntD = gtk.Entry(3)
    self.dacIntD.set_name("dacIntD")
    self.dacIntD.connect("changed",self.dacIntChanged)
    self.dacIntBox.pack_start(self.dacIntD,True,True,10)

    self.dacHexBox = gtk.HBox()
    self.dacHexLabel = gtk.Label("Hex")
    self.dacHexBox.pack_start(self.dacHexLabel,True,True,10)
    self.dacHexA = gtk.Entry(2)
    self.dacHexA.set_name("dacHexA")
    self.dacHexA.connect("changed",self.dacHexChanged)
    self.dacHexBox.pack_start(self.dacHexA,True,True,10)
    self.dacHexB = gtk.Entry(2)
    self.dacHexB.set_name("dacHexB")
    self.dacHexB.connect("changed",self.dacHexChanged)
    self.dacHexBox.pack_start(self.dacHexB,True,True,10)
    self.dacHexC = gtk.Entry(2)
    self.dacHexC.set_name("dacHexC")
    self.dacHexC.connect("changed",self.dacHexChanged)
    self.dacHexBox.pack_start(self.dacHexC,True,True,10)
    self.dacHexD = gtk.Entry(2)
    self.dacHexD.set_name("dacHexD")
    self.dacHexD.connect("changed",self.dacHexChanged)
    self.dacHexBox.pack_start(self.dacHexD,True,True,10)

    self.dacBinBox = gtk.HBox()
    self.dacBinLabel = gtk.Label("Bin")
    self.dacBinBox.pack_start(self.dacBinLabel,True,True,10)
    self.dacBinA = gtk.Entry(8)
    self.dacBinA.set_name("dacBinA")
    self.dacBinA.connect("changed",self.dacBinChanged)
    self.dacBinBox.pack_start(self.dacBinA,True,True,10)
    self.dacBinB = gtk.Entry(8)
    self.dacBinB.set_name("dacBinB")
    self.dacBinB.connect("changed",self.dacBinChanged)
    self.dacBinBox.pack_start(self.dacBinB,True,True,10)
    self.dacBinC = gtk.Entry(8)
    self.dacBinC.set_name("dacBinC")
    self.dacBinC.connect("changed",self.dacBinChanged)
    self.dacBinBox.pack_start(self.dacBinC,True,True,10)
    self.dacBinD = gtk.Entry(8)
    self.dacBinD.set_name("dacBinD")
    self.dacBinD.connect("changed",self.dacBinChanged)
    self.dacBinBox.pack_start(self.dacBinD,True,True,10)



    # make frame for DAC
    frameDAC = gtk.Frame("DAC")
    vbox2 = gtk.VBox()
    # vbox2.set_border_width(5)
    frameDAC.add(vbox2)
    
    vbox2.pack_start(self.dacIntBox,True,True,5)
    vbox2.pack_start(self.dacHexBox,True,True,5)
    vbox2.pack_start(self.dacBinBox,True,True,5)
    self.mainBox.pack_start(frameDAC)
    # options layout
    self.optionBox = gtk.HBox()
    self.btnZero = gtk.Button("Zero")
    self.btnZero.connect("clicked", self.zeroDAC)
    self.btnSet = gtk.Button("Set")
    self.btnSet.connect("clicked", self.setDAC)
    self.btnReg = gtk.Button("Test")
    self.btnReg.connect("clicked",self.setRegTest)
    self.optionBox.pack_start(self.btnReg)
    self.optionBox.pack_start(self.btnSet)
    self.optionBox.pack_start(self.btnZero)
    
    self.mainBox.pack_start(self.optionBox)
    self.testBox = gtk.Entry()
    self.mainBox.pack_start(self.testBox)

    self.area = gtk.DrawingArea()
    self.area.set_size_request(100,100)
    #self.area.connect("expose-event", self.area_expose_cb)
    self.mainBox.pack_start(self.area)

    # add main layout to the window
    self.window.add(self.mainBox)
    self.window.show_all()


  def main(self):
      gtk.main()

if __name__ == "__main__":
    base = Base()
    base.main()
