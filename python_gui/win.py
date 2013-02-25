#!/usr/bin/python

import pygtk
pygtk.require('2.0')
import gtk

class Base:
  def destroy(self, widget, data=None):
    #this is where you put stuff
    print "Thanks for playing!"
    gtk.main_quit()

  def handleButton(self, widget):
    print widget.get_name()

  def handleRegButton(self,widget):
    if widget.get_label() == "0":
      widget.set_label("1")
    else:
      widget.set_label("0")

  def shiftIn(self, widget):
    #do nothing for now

  def myhide(self, widget):
    if self.button1.get_visible() : 
      self.button1.hide()
      self.exitLabel.set_text("Button is gone!")
    else:
      self.button1.show()
      self.exitLabel.set_text("Button is Back!")

  def __init__(self):
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.window.set_position(gtk.WIN_POS_CENTER)
    self.window.set_size_request(500,500)
    self.window.set_title("Pocasa - Pi")

    self.reg01 = gtk.Button("0")
    self.reg01.connect("clicked", self.handleRegButton)


    self.button1 = gtk.Button("Exit")
    self.button1.connect("clicked", self.destroy)
    self.button1.set_tooltip_text("This button closes this window")
    self.button2 = gtk.Button("Toggle")
    self.button2.connect("clicked", self.handleButton)
    self.button2.set_name("button2")
    self.exitLabel = gtk.Label("this will exit! -->")

    self.mainBox = gtk.VBox()

    self.buttonBox = gtk.HBox()
    self.labelBox = gtk.HBox()

    for i in range(10):
      button = gtk.Button("0")
      button.set_name("reg_"+str(i))
      button.connect("clicked",self.handleRegButton)
      self.buttonBox.pack_start(button)
      label = gtk.Label("0")
      label.set_name("label_" + str(i))
      self.labelBox.pack_start(label)

    
    self.reg_01 = gtk.Button("0")
    self.reg_01.connect("clicked", self.handleRegButton)
    self.buttonBox.pack_start(self.reg_01)
    
    self.reg_01 = gtk.Button("0")
    self.reg_01.connect("clicked", self.handleRegButton)
    self.buttonBox.pack_start(self.reg_01)
    
    self.reg_01 = gtk.Button("0")
    self.reg_01.connect("clicked", self.handleRegButton)
    self.buttonBox.pack_start(self.reg_01)
    
    self.reg_01 = gtk.Button("0")
    self.reg_01.connect("clicked", self.handleRegButton)
    self.buttonBox.pack_start(self.reg_01)
    
    self.mainBox.pack_start(self.buttonBox)
    self.mainBox.pack_start(self.labelBox)
    self.box1 = gtk.HBox()
    self.box1.pack_start(self.exitLabel)
    self.box1.pack_start(self.button1)
    self.mainBox.pack_start(self.box1)

    self.box2 = gtk.HBox()
    self.box2.pack_start(self.button2)
    self.mainBox.pack_start(self.box2)

    self.window.add(self.mainBox)


    self.window.show_all()
    self.window.connect("destroy", self.destroy)

  def main(self):
    gtk.main()

if __name__ == "__main__":
  base = Base()
  base.main()
