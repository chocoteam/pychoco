#ifndef __BACKEND_H
#define __BACKEND_H

#if defined(__cplusplus)
extern "C" {
#endif

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

//

#if defined(__cplusplus)
}
#endif
#endif