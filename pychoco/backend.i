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

void* get_solver(void*);

// Solver API

void* find_solution(void*);

void show_statistics(void*);

void show_short_statistics(void*);

// Solution API

int get_int_val(void*, void*);

// Intvars

void* intvar_sii(void*, char*, int, int);

void* intvar_ii(void*, int, int);

char* get_intvar_name(void*);

int get_intvar_lb(void*);

int get_intvar_ub(void*);

// Constraints

char* get_constraint_name(void*);

void post(void*);

void* arithm_iv_cst(void*, void*, char*, int);

void* arithm_iv_iv(void*, void*, char*, void*);

void* arithm_iv_iv_cst(void*, void*, char*, void*, char*, int);

void* arithm_iv_iv_iv(void*, void*, char*, void*, char*, void*);

void* member_iv_iarray(void*, void*, void*);

void* member_iv_i_i(void*, void*, int, int);

void* allDifferent(void*, void*);

void* mod_iv_i_i(void*, void*, int, int);

void* mod_iv_i_iv(void*, void*, int, void*);

void* mod_iv_iv_iv(void*, void*, void*, void*);

void* not(void*, void*);

void* not_member_iv_iarray(void*, void*, void*);

void* not_member_iv_i_i(void*, void*, int, int);

void* absolute(void*, void*, void*);

void* distance_iv_iv_i(void*, void*, void*, char*, int);

void* distance_iv_iv_iv(void*, void*, void*, char*, void*);

void* element_iv_iarray_iv_i(void*, void*, void*, void*, int);

void* element_iv_ivarray_iv_i(void*, void*, void*, void*, int);

void* square(void*, void*, void*);

void* times_iv_i_iv(void*, void*, int, void*);

void* times_iv_iv_i(void*, void*, void*, int);

void* times_iv_iv_iv(void*, void*, void*, void*);

void* div_(void*, void*, void*, void*);

void* max_iv_iv_iv(void*, void*, void*, void*);

void* max_iv_ivarray(void*, void*, void*);

void* min_iv_iv_iv(void*, void*, void*, void*);

void* min_iv_ivarray(void*, void*, void*);

void* all_different(void*, void*);

// Array API

void* create_intvar_array(int);

int intvar_array_length(void*);

void intvar_array_set(void*, void*, int);

void* create_int_array(int);

int int_array_length(void*);

void int_array_set(void*, int, int);
