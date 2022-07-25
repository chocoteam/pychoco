#include <stdlib.h>
#include <stdio.h>

#include <libchoco_capi.h>
#include <graal_isolate.h>

#ifdef _WIN32
#define THREAD_LOCAL __declspec( thread )
#else
#define THREAD_LOCAL __thread 
#endif

// single graalVM isolate
static graal_isolate_t *isolate = NULL;

// thread local variable
static THREAD_LOCAL graal_isolatethread_t *thread = NULL;

// library init
void chocosolver_init() {
    // do we need to synchronize here, or does the GIL protect us?
    if (isolate == NULL) { 
        // create isolate and attach thread
        if (graal_create_isolate(NULL, &isolate, &thread) != 0) {
            fprintf(stderr, "graal_create_isolate error\n");
            exit(EXIT_FAILURE);
        }
    } else if (thread == NULL) {
        // attach thread
        if (graal_attach_thread(isolate, &thread) != 0) { 
            fprintf(stderr, "graal_attach_thread error\n");
            exit(EXIT_FAILURE);
        }
    }
}

#define LAZY_THREAD_ATTACH \
    if (thread == NULL) { \
        if (graal_attach_thread(isolate, &thread) != 0) {    \
            fprintf(stderr, "graal_attach_thread error\n");  \
            exit(EXIT_FAILURE);                              \
        }                                                    \
    }

// library cleanup
void chocosolver_cleanup() {
    // let the JVM cleanup for itself
}

int chocosolver_is_initialized() { 
    return thread != NULL && isolate != NULL;
}

// Model API

void* create_model(char* name) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ModelApi_createModel(thread, name);
}

char* get_model_name(void* modelHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ModelApi_getName(thread, modelHandle);
}

// Intvars

void* intvar_sii(void* modelHandle, char* name, int lb, int ub) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ModelApi_intVar_sii(thread, modelHandle, name, lb, ub);
}

void* intvar_ii(void* modelHandle, int lb, int ub) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ModelApi_intVar_ii(thread, modelHandle, lb, ub);
}

char* get_intvar_name(void* varHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_IntVarApi_getName(thread, varHandle);
}

int get_intvar_lb(void* varHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_IntVarApi_getLB(thread, varHandle);
}

int get_intvar_ub(void* varHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_IntVarApi_getUB(thread, varHandle);
}

// Constraints

char* get_constraint_name(void* constraintHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_getName(thread, constraintHandle);
}

void* all_different(void* modelHandle, void* vars) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ModelApi_allDifferent(thread, modelHandle, vars);
}

void post(void* constraintHandle) {
    LAZY_THREAD_ATTACH
    Java_org_chocosolver_capi_ConstraintApi_post(thread, constraintHandle);
}

void solve(void* modelHandle) {
    LAZY_THREAD_ATTACH
    Java_org_chocosolver_capi_ModelApi_solve(thread, modelHandle);
}

// Array API

void* create_intvar_array(int size) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ArrayApi_intVar_create(thread, size);
}

int intvar_array_length(void* arrayHande) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ArrayApi_intVar_length(thread, arrayHande);
}

void intvar_array_set(void* arrayHande, void* intVarHande, int index) {
    LAZY_THREAD_ATTACH
    Java_org_chocosolver_capi_ArrayApi_intVar_set(thread, arrayHande, intVarHande, index);
}