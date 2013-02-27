// Created by Ryan Hatfield
// http://tophathacker.com
// tophathacker@gmail.com

#include <Python.h>
#include <wiringPi.h>

//define methods (not already defined by python.h)
static int setupInput(const int pin);
static int setupOutput(const int pin);
static int shiftbits(uint16_t input);
static int pauseMe(long unsigned int time);

static PyObject* setup_pins(PyObject* self, PyObject* args)
{
  if(wiringPiSetup() == -1)
    exit(1);

  // pin defines
  const int ClockPin = 0;
  const int DataPin = 1;
  const int DumpPin = 2;
  const int inputX = 7;
  const int inputY = 3;

  // setup inputs
  setupInput(inputX);
  setupInput(inputY);

  // setup outputs
  setupOutput(ClockPin);
  setupOutput(DataPin);
  setupOutput(DumpPin);

  Py_RETURN_NONE;
}

static int setupInput(const int pin)
{
  // setup input pin
  pinMode(pin, INPUT);
  return 0;
}

static int setupOutput(const int pin)
{
  // setup output and pull low
  pinMode(pin,OUTPUT);
  digitalWrite(pin,0);
  return 0;
}

static PyObject* shift_out(PyObject* self, PyObject* args)
{
		uint16_t input = 65534;
		if(!PyArg_ParseTuple(args,"i",&input))
			return NULL;
    
    shiftbits(input);

		Py_RETURN_NONE;

}

static int shiftbits(uint16_t input)
{
  const int clock = 0;
  const int data = 1;
  const int dump = 2;

  int i;

  for(i=0; i < 16; i++)
  {
    digitalWrite(data,input & 1);
    input >>= 1;
    digitalWrite(clock,1);
    digitalWrite(clock,0);
  }

  digitalWrite(dump,1);
  digitalWrite(dump,0);
  return 0;
}

static int pauseMe(long unsigned int time)
{
  int i;
  for(i=0; i<time; i++);
  return 0;
}

static PyObject* readXY(PyObject *self, PyObject *args)
{
  uint16_t oldreg = 65534;
  if(!PyArg_ParseTuple(args,"ii",oldreg))
    return NULL;

  const int selectPin = 7;
  const int clockPin = 4;
  const int pinX = 7;
  const int pinY = 3;

  // bring selectPin low?
  oldreg &= ~(1 << selectPin);
  shiftbits(oldreg);

  // dummy Clock
  oldreg |= 1 << clockPin;
  shiftbits(oldreg);
  oldreg &= ~(1 << clockPin);
  shiftbits(oldreg);
  oldreg |= 1 << clockPin;
  shiftbits(oldreg);
  oldreg &= ~(1 << clockPin);
  shiftbits(oldreg);

  long unsigned int x = 0,y = 0;
  int i;
  for(i=11; i>0; i--)
  {
    oldreg |= 1 << clockPin;
    shiftbits(oldreg);
    oldreg &= ~(1 << clockPin);
    shiftbits(oldreg);

    x |= digitalRead(pinX) << i;
    y |= digitalRead(pinY) << i;
  }

  oldreg |= 1 << selectPin;
  shiftbits(oldreg);

  return Py_BuildValue("ii",x,y);
}

static PyMethodDef shiftMethods[] =
{
  {"shift_out",shift_out,METH_VARARGS,"shift out the bits"},
  {"setup_pins",setup_pins,METH_VARARGS,"setup input/output pins"},
  {"readXY",readXY,METH_VARARGS,"something"},
  {NULL, NULL, 0, NULL}
};
   
PyMODINIT_FUNC
    
initshift(void)
{
  (void) Py_InitModule("shift", shiftMethods);
}
