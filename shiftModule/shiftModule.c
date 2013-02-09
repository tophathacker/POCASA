#include <Python.h>

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
  {"print_something", print_something, METH_VARARGS, "Print something."},
  {"readXY",readXY,METH_VARARGS,"something"},
  {NULL, NULL, 0, NULL}
};
   
PyMODINIT_FUNC
    
initshift(void)
{
  (void) Py_InitModule("shift", shiftMethods);
}
