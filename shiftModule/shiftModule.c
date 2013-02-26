#include <Python.h>

static PyObject* print_something(PyObject* self, PyObject* args)
{
  const char* name;
  
  if (!PyArg_ParseTuple(args, "s", &name))
    return NULL;
  
  printf("Hello %s!\n", name);
  
  Py_RETURN_NONE;
}
  
static PyMethodDef shiftMethods[] =
{
  {"print_something", print_something, METH_VARARGS, "Print something."},
  {NULL, NULL, 0, NULL}
};
   
PyMODINIT_FUNC
    
initshift(void)
{
  (void) Py_InitModule("shift", shiftMethods);
}
