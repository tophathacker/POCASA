#!/usr/bin/python

# following the hello world tutorials on pygtk.org wiki 

import pygtk
pygtk.require('2.0')
import gtk

class HelloWorld:
  # this is a callback function. the data arguments are ignored
  # in this example. More on callbacks below.
  def hello(self, widget, data=None):
    print "Hello World"

  def delete_event(self, widget, event, data=None):
    # if you return false, the delete event will kill
    # the app, if you return true, you don't want the window
    # destroyed. 
    print "destroy event occurred"

    return False

  # Another callback
  def destroy(self, widget, data=None):
    gtk.main_quit()

  def __init__(self):
    # create a new window
    self.window1 = gtk.Window(gtk.WINDOW_TOPLEVEL)

    # when the window is given the "delete_event" signal (this is given
    # by the window manager, usually by the "close" option, or on the
    # titlebar), we ask it to call the delete_event () function
    # as defined above. the data passed to the callback
    # function is NULL and is ignored in the callback function.
    self.window1.connect("delete_event",self.delete_event)

    # here we connect the "destroy" event to a signal handler.
    # this event occurs when we call gtk_widget_destroy() on the window,
    # or if we return FALSE in the "delete_event" callback.
    self.window1.connect("destroy",self.destroy)

    # Sets the border width of the window
    self.window1.set_border_width(20)

    # Creates a new button with the lable "Hello World"
    self.button1 = gtk.Button("Hello World")

    # when the button recieves the "clicked" signal, it will call the
    # function hello() passing it None as an argument. the hello()
    # function is defined above.
    self.button1.connect("clicked", self.hello, None)

    # this will cause the window to be destroyed by calling
    # gtk_widget_destroy(window) when "clicked". again, the destroy
    # signal could come from here, or the window manager.
    #self.button1.connect_object("clicked",gtk.Widget.destroy, self.window1)
    
    self.window1.add(self.button1)
    # the final step is to display this newly created widget
    self.button1.show()

    self.window1.set_size_request(200,200)
    # and the window
    self.window1.show()

  def main(self):
    #all PyGTK applications must have a gtk.main() Control ends here
    # and waits for an event to occur (like a key press or mouse event)
    gtk.main()

# if the program is run directly or passed as an argument to the python
# interpreter then create a helloworld instance and show it
if __name__ == "__main__":
  hello = HelloWorld()
  hello.main()
