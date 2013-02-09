#include <Python.h>
#include <wiringPi.h>

//define methods (not already defined by python.h)
static int setupInput(const int pin);
static int setupOutput(const int pin);

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
  	//  int shiftOut(int clock, int data, int dump, char input[])
    const int clock = 0;
		const int data = 1;
		const int dump = 2;

    int i; 
		uint16_t input = 65534;
		if(!PyArg_ParseTuple(args,"i",&input))
			return NULL;
   
	 	printf("%u",input);
		 
    for(i=0; i < 16; i++)
    {
      digitalWrite(data,input & 1);
			//printf("%u",input & 1);
			input >>= 1;
      digitalWrite(clock,1);
      //pauseMe(10);
      digitalWrite(clock,0);
      //pauseMe(10);
    }
    
    digitalWrite(dump,1);
    //pauseMe(10);
    digitalWrite(dump,0);
    //pauseMe(200);
    
		Py_RETURN_NONE;

}

static PyObject* print_something(PyObject* self, PyObject* args)
{
  long unsigned int i; 
  
  if (!PyArg_ParseTuple(args, "i", &i))
    return NULL;
  
  printf("Hello %lu!\n", i);
  
  Py_RETURN_NONE;
}



static PyObject* readXY(PyObject *self, PyObject *args)
{
  long unsigned int x,y;

  if(!PyArg_ParseTuple(args, "ii", &x, &y))
    return NULL;
  return Py_BuildValue("ii",x,y);
}

static PyMethodDef shiftMethods[] =
{
  {"shift_out",shift_out,METH_VARARGS,"shift out the bits"},
  {"setup_pins",setup_pins,METH_VARARGS,"setup input/output pins"},
  {"print_something", print_something, METH_VARARGS, "Print something."},
  {"readXY",readXY,METH_VARARGS,"something"},
  {NULL, NULL, 0, NULL}
};
   
PyMODINIT_FUNC
    
initshift(void)
{
  (void) Py_InitModule("shift", shiftMethods);
}
