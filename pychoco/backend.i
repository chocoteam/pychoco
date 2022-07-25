%module backend

%{
#define SWIG_FILE_WITH_INIT
#include "backend.h"
%}


%include <typemaps.i>


// custom typemap to append void** types to the result
%typemap(in,numinputs=0,noblock=1) void **OUTPUT ($*1_ltype temp) {
    $1 = &temp;
}

%typemap(argout,noblock=1) void **OUTPUT {
    %append_output(SWIG_NewPointerObj(*$1, $*1_descriptor, SWIG_POINTER_NOSHADOW | %newpointer_flags));
}

%typemap(in,numinputs=0,noblock=1) char **OUTPUT ($*1_ltype temp) {
    $1 = &temp;
}

%typemap(argout,noblock=1) char **OUTPUT {
    %append_output(SWIG_FromCharPtr(($*1_ltype)*$1));
}

// convert a long to a void function pointer
%typemap(in) void *LONG_TO_FPTR { 
    $1 = PyLong_AsVoidPtr($input);    
}

// convert bytearray to c-string
%typemap(in) char *BYTEARRAY {
    if ($input != Py_None) { 
        if (!PyByteArray_Check($input)) {
            SWIG_exception_fail(SWIG_TypeError, "in method '" "$symname" "', argument "
                       "$argnum"" of type '" "$type""'");
        }
        $1 = (char*) PyByteArray_AsString($input);
    } else { 
        $1 = (char*) 0;
    }
}

// library init

void chocosolver_init();

void chocosolver_cleanup();

int chocosolver_is_initialized();

// Model API

void* create_model(char*);

char* get_model_name(void*);

// Intvars

void* intvar_sii(void*, char*, int, int);

void* intvar_ii(void*, int, int);

char* get_intvar_name(void*);

int get_intvar_lb(void*);

int get_intvar_ub(void*);

// Constraints

char* get_constraint_name(void*);

void* all_different(void*, void*);

void post(void*);

void solve(void*);

// Array API

void* create_intvar_array(int);

int intvar_array_length(void*);

void intvar_array_set(void*, void*, int);