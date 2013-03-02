#!/usr/bin/env python

from gi.repository import Gtk

class POCASA_Pi():
 
  def on_window1_destory(self,widget):
    Gtk.main_quit()

  def __init__(self):
    builder = Gtk.Builder()
    builder.add_from_file("mainui.xml")
    #handlers = {
    #  "on_window1_destroy_event":Gtk.main_quit(),
    #  "on_window1_destroy":Gtk.main_quit()
    #}
    builder.connect_signals(self)
    self.window = builder.get_object("window1")
    self.clicks = [];
     
  def destroy(widget,self):
    Gtk.main_quit()

  def on_area_press(self,widget,event):
    print "on_area_press " + widget.get_name()
    self.clicks.append([event.x,event.y])
    widget.queue_draw()

    return True

  def on_area_draw(self, drawing_area, cairo_context):
    print "on draw" ,drawing_area.get_name()
    cairo_context.move_to(50,50)
    for point in self.clicks:
      cairo_context.line_to(point[0],point[1])
    cairo_context.stroke()

  def manualChanged(self,widget):
    print widget.get_text()

win = POCASA_Pi()
win.window.show_all()
Gtk.main()
