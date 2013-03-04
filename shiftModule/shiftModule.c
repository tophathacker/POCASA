// Created by Ryan Hatfield
// http://tophathacker.com
// tophathacker@gmail.com

#include <Python.h>
#include <wiringPi.h>
#include <time.h>

//define methods (not already defined by python.h)
static int _setupInput(const int pin);
static int _setupOutput(const int pin);
static uint16_t _shiftbits(uint16_t input);
static int _pauseMe(long unsigned int time);
static uint32_t _getadc(uint16_t oldreg);

// pin defines
const int ClockPin = 0;
const int DataPin = 1;
const int DumpPin = 2;
const int inputX = 7;
const int inputY = 6;

static PyObject* setup_pins(PyObject* self, PyObject* args)
{
  if(wiringPiSetup() == -1)
    exit(1);

  // setup inputs
  _setupInput(inputX);
  _setupInput(inputY);

  // setup outputs
  _setupOutput(ClockPin);
  _setupOutput(DataPin);
  _setupOutput(DumpPin);

  Py_RETURN_NONE;
}

static int _setupInput(const int pin)
{
  // setup input pin
  pinMode(pin, INPUT);
  return 0;
}

static int _setupOutput(const int pin)
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
    
  input = _shiftbits(input);
  return Py_BuildValue("i",input);
  //Py_RETURN_NONE;
}

static uint16_t _shiftbits(uint16_t input)
{
  const int clock = 0;
  const int data = 1;
  const int dump = 2;

  int i;
  // did i fix this?
  for(i=15; i >= 0; i--)
  {
    digitalWrite(data,(input >> i) & 1);
    digitalWrite(clock,1);
    digitalWrite(clock,0);
  }

  digitalWrite(dump,1);
  digitalWrite(dump,0);
  //_reg = input;
  return input;
}

static int _pauseMe(long unsigned int time)
{
  int i;
  for(i=0; i<time; i++);
  return 0;
}

static uint32_t _getadc(uint16_t oldreg)
{
  const int AdcClock = 4;
  const int AdcCS = 7;

  uint32_t returnValue = 0;
  
  oldreg &= ~(1 << AdcClock); // make sure clock is low
  _shiftbits(oldreg);
  oldreg &= ~(1 << AdcCS);    // make pull CS low
  _shiftbits(oldreg);
  nanosleep((struct timespec[]){{0, 12000}}, NULL);
  oldreg |= 1 << AdcClock;
  _shiftbits(oldreg);
  oldreg &= ~(1 << AdcClock); 
  _shiftbits(oldreg);
  oldreg |= 1 << AdcClock;
  _shiftbits(oldreg);
  oldreg &= ~(1 << AdcClock);
  _shiftbits(oldreg);

  int i;
  for (i = 15; i >=0; i--)
  {
    oldreg |= 1 << AdcClock;
    _shiftbits(oldreg);
    oldreg &= ~(1 << AdcClock);
    _shiftbits(oldreg);
    returnValue |= digitalRead(inputX) << i;
    returnValue |= digitalRead(inputY) << (i + 16);
  }
  
  oldreg |= 1 << AdcCS; // pull CS high again
  _shiftbits(oldreg);
  return returnValue;
}

static PyObject* get_adc(PyObject *self, PyObject *args)
{
  uint16_t x = 0;
  uint16_t y = 0;

  uint16_t oldreg = 0;
  if(!PyArg_ParseTuple(args,"k",&oldreg))
    return NULL;
 
  uint32_t xy = _getadc(oldreg);
  printf("from c: %lu",xy);
  int i;
  for (i = 31; i >= 16; i--)
  {
    x |= ((xy >> i) & 1) << (i - 16);
  }
  for (i = 15; i >= 0; i--)
  {
    y |= ((xy >> i) & 1) << i;
  }
  return Py_BuildValue("ii",x,y);
}

static uint16_t _setdac(uint16_t inoldreg, uint32_t newsetting)
{
  const int select = 6;
  const int clock = 3;
  const int data = 2;
  uint16_t oldreg = 0;  // should be inoldreg, but i'm testing.
  
  oldreg &= ~(1 << clock); // make sure clock is low
  _shiftbits(oldreg);
  oldreg &= ~(1 << select); // set select pin low
  _pauseMe(10000);
  _shiftbits(oldreg);
  
  int j;
  for (j = 31; j >= 0; j--)
  {
    if ((newsetting >> j) & 1) // set data bit
      oldreg |= 1 << data;
    else
      oldreg &= ~(1<<data);
    _shiftbits(oldreg);
    oldreg |= 1 << clock; // set clock high
    _shiftbits(oldreg);
    oldreg &= ~(1<<clock); // set clock low
    _shiftbits(oldreg);
  }
  oldreg |= 1 << select; // set select high again
  _shiftbits(oldreg);
  return oldreg;
}
static PyObject* set_dac(PyObject *self, PyObject *args)
{
  uint16_t oldreg = 0;
  uint32_t newsetting = 0;
  if(!PyArg_ParseTuple(args,"kk",&oldreg,&newsetting))
    return NULL;
  oldreg = _setdac(oldreg,newsetting);
  return Py_BuildValue("i",oldreg);
}

static PyObject* read_xy(PyObject *self, PyObject *args)
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
  _shiftbits(oldreg);

  // dummy Clock
  oldreg |= 1 << clockPin;
  _shiftbits(oldreg);
  oldreg &= ~(1 << clockPin);
  _shiftbits(oldreg);
  oldreg |= 1 << clockPin;
  _shiftbits(oldreg);
  oldreg &= ~(1 << clockPin);
  _shiftbits(oldreg);

  long unsigned int x = 0,y = 0;
  int i;
  for(i=11; i>0; i--)
  {
    oldreg |= 1 << clockPin;
    _shiftbits(oldreg);
    oldreg &= ~(1 << clockPin);
    _shiftbits(oldreg);

    x |= digitalRead(pinX) << i;
    y |= digitalRead(pinY) << i;
  }

  oldreg |= 1 << selectPin;
  _shiftbits(oldreg);

  return Py_BuildValue("ii",x,y);
}

static PyMethodDef shiftMethods[] =
{
  {"shift_out",shift_out,METH_VARARGS,"shiftout"},
  {"setup_pins",setup_pins,METH_VARARGS,"setup input/output pins"},
  {"read_xy",read_xy,METH_VARARGS,"something"},
  {"set_dac",set_dac,METH_VARARGS,"something2"},
  {"get_adc",get_adc,METH_VARARGS,"something3"},
  {NULL, NULL, 0, NULL}
};
   
PyMODINIT_FUNC
    
initshift(void)
{
  (void) Py_InitModule("shift", shiftMethods);
}
