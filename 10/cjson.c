#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <Python.h>


// gcc cjson.c -I/usr/include/python3.10

void parse_string(char* string, int begin, char* key, int* i) {
   if (string[begin] != '\"') {
      exit(1);
   }

   *i = begin + 1;

   while (string[*i] != '\"') {
      (*i)++;
   }

   strncpy(key, string + begin + 1, *i - begin - 1);
   key[*i - begin - 1] = '\0';
   
   (*i)++;

   while ((string[*i] == ':') || (isspace(string[*i]))) {
      (*i)++;
   }
}

void parse_number(char* string, int begin, int* value, int* i) {
   *i = begin;

   while (isdigit(string[*i])) {
      (*i)++;
   }

   char num_str[*i - begin + 1];
   strncpy(num_str, string + begin, *i - begin);
   num_str[*i - begin] = '\0';
   *value = atoi(num_str);
}

void parse_key(char* string, int begin, char* key, int* i) {
   parse_string(string, begin, key, i);
}

void parse_value(char* string, int begin, void** value, int* i) {
   if (isdigit(string[begin])) {
      int* num_ptr = malloc(sizeof(int));
      parse_number(string, begin, num_ptr, i);
      *value = num_ptr;
   } else {
      char* str_ptr = malloc(256*sizeof(char));
      parse_string(string, begin, str_ptr, i);
      *value = str_ptr;
   }
}

int skip_symbols(char* string, int index) {
   while (isspace(string[index]) || string[index] == ',') {
      index++;
   }
   return index;
}

static PyObject* cjson_loads(PyObject* self, PyObject* args)
{
   char* string;
   if (!PyArg_ParseTuple(args, "s", &string)) {
      printf("ERROR: Failed to parse string\n");
      return NULL;
   }

   // printf("\n\nCurrent command: %s\n", string);

   if (string[0] != '{' || string[strlen(string)-1] != '}') {
      printf("ERROR");
      exit(1);
   }
    
   PyObject *dict = NULL;
   if (!(dict = PyDict_New())) {
      printf("ERROR: Failed to create Dict Object\n");
      return NULL;
   }

   int index = 1;
   while (index < (int) strlen(string) - 1) {
      PyObject *py_key = NULL;
      PyObject *py_value = NULL;

      char key[256];
      int i = index;
      parse_key(string, index, key, &i);

      if (!(py_key = Py_BuildValue("s", key))) {
         printf("ERROR: Failed to build string value\n");
         return NULL;
      }  

      void* value;
      parse_value(string, i, &value, &i);
      if (isdigit(string[i-1])) {

         if (!(py_value = Py_BuildValue("i", *((int*)value)))) {
            printf("ERROR: Failed to build integer value\n");
            return NULL;
         }

      } else {

         if (!(py_value = Py_BuildValue("s", (char*)value))) {
            printf("ERROR: Failed to build string value\n");
            return NULL;
         }
      }

      if (PyDict_SetItem(dict, py_key, py_value) < 0) {
         printf("ERROR: Failed to set item\n\n\n");
         return NULL;
      }

      index = skip_symbols(string, i);
   }

   return dict;
}

char* concatenate(const char* str1, const char* str2) {
   int len1 = strlen(str1);
   int len2 = strlen(str2);
   int i, j;

   char* result = (char*) malloc((len1 + len2 + 1) * sizeof(char));

   for (i = 0; i < len1; i++) {
      result[i] = str1[i];
   }

   for (j = 0; j < len2; j++) {
      result[i + j] = str2[j];
   }

   result[i + j] = '\0';

   return result;
}

static PyObject* cjson_dumps(PyObject* self, PyObject* dict_obj)
{

   PyObject* dict;

   if (!PyArg_ParseTuple(dict_obj, "O", &dict)) {
      printf("ERROR: Failed to parse dict\n");
      return NULL;
   }
   
   if (!PyDict_Check(dict)) {
      PyErr_SetString(PyExc_TypeError, "Argument must be a dictionary");
      return NULL;
   }

   PyObject* key_obj;
   PyObject* value_obj;
   Py_ssize_t pos = 0;

   int i = 0;
   char* result = "{";
   while (PyDict_Next(dict, &pos, &key_obj, &value_obj)) {
      if (i != 0)
        result = concatenate(result, ", ");
      char* key = PyUnicode_AsUTF8(key_obj);

      result = concatenate(result, "\"");
      result = concatenate(result, key);
      result = concatenate(result, "\": ");

      if (PyUnicode_Check(value_obj)) {
        char* value = PyUnicode_AsUTF8(value_obj);
        result = concatenate(result, "\"");
        result = concatenate(result, value);
        result = concatenate(result, "\"");
      } else {
        int num = (int) PyLong_AsLong(value_obj);
        char* arr;
        int size = snprintf(NULL, 0, "%d", num) + 1;
        arr = (char*) malloc(size);

        sprintf(arr, "%d", num);
        result = concatenate(result, arr);
      }
      ++i;
   }
   result = concatenate(result, "}");
   PyObject* result_py = PyUnicode_FromString(result);
   return result_py;

}

static PyMethodDef methods[] = {
   {"loads", cjson_loads, METH_VARARGS, "Json to Dict converter."},
   {"dumps", cjson_dumps, METH_VARARGS, "Dict to Json converter."},
   {NULL, NULL, 0, NULL}
};

static PyModuleDef cjsonmodule = {
   PyModuleDef_HEAD_INIT,
   "cjson",
   "Module for load and dump json.",
   -1,
   methods
};

PyMODINIT_FUNC PyInit_cjson(void) {
   return PyModule_Create( &cjsonmodule );
}
