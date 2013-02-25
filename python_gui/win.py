#!/usr/bin/python

import pygtk
pygtk.require('2.0')
import gtk

class Base:
  def destroy(self, widget, data=None):
    #this is where you put stuff
    print "Thanks for playing!"
    gtk.main_quit()

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

    self.button1 = gtk.Button("Exit")
    self.button1.connect("clicked", self.destroy)
    self.button1.set_tooltip_text("This button closes this window")
    self.button2 = gtk.Button("Toggle")
    self.button2.connect("clicked", self.myhide)
    self.exitLabel = gtk.Label("this will exit! -->")

    self.mainBox = gtk.VBox()

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
