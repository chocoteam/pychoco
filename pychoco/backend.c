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

void* get_solver(void* modelHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ModelApi_getSolver(thread, modelHandle);
}

// Solver API

void* find_solution(void* solverHandle, void* stopArrayHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_SolverApi_findSolution(thread, solverHandle, stopArrayHandle);
}

void* find_all_solutions(void* solverHandle, void* stopArrayHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_SolverApi_findAllSolutions(thread, solverHandle, stopArrayHandle);
}

void* find_optimal_solution(void* solverHandle, void* objectiveVarHandle, _Bool maximize, void* stop) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_SolverApi_findOptimalSolution(thread, solverHandle, objectiveVarHandle, maximize, stop);
}

void* find_all_optimal_solutions(void* solverHandle, void* objectiveVarHandle, _Bool maximize, void* stop) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_SolverApi_findAllOptimalSolutions(thread, solverHandle, objectiveVarHandle, maximize, stop);
}

void show_statistics(void* solverHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_SolverApi_showStatistics(thread, solverHandle);
}

void show_short_statistics(void* solverHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_SolverApi_showShortStatistics(thread, solverHandle);
}

// Criterion API

void* time_counter(void* modelHandle, long timeLimitNano) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_CriterionApi_time_counter(thread, modelHandle, timeLimitNano);
}

void* solution_counter(void* modelHandle, long solutionLimit) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_CriterionApi_solution_counter(thread, modelHandle, solutionLimit);
}

void* node_counter(void* modelHandle, long nodeLimit) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_CriterionApi_node_counter(thread, modelHandle, nodeLimit);
}

void* fail_counter(void* modelHandle, long failLimit) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_CriterionApi_fail_counter(thread, modelHandle, failLimit);
}

void* restart_counter(void* modelHandle, long restartLimit) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_CriterionApi_restart_counter(thread, modelHandle, restartLimit);
}

void* backtrack_counter(void* modelHandle, long backtrackLimit) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_CriterionApi_backtrack_counter(thread, modelHandle, backtrackLimit);
}

// Solution API

int get_int_val(void* solutionHandle, void* intVarHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_SolutionApi_getIntVal(thread, solutionHandle, intVarHandle);
}

// Intvars

void* intvar_sii(void* modelHandle, char* name, int lb, int ub) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_IntVarApi_intVar_sii(thread, modelHandle, name, lb, ub);
}

void* intvar_ii(void* modelHandle, int lb, int ub) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_IntVarApi_intVar_ii(thread, modelHandle, lb, ub);
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

// Boolvars

void* boolvar_s(void* modelHandle, char* name) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_BoolVarApi_boolVar_s(thread, modelHandle, name);
}

void* boolvar(void* modelHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_BoolVarApi_boolVar(thread, modelHandle);
}

void* boolvar_b(void* modelHandle, _Bool value) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_BoolVarApi_boolVar_b(thread, modelHandle, value);
}

void* boolvar_sb(void* modelHandle, char* name, _Bool value) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_BoolVarApi_boolVar_sb(thread, modelHandle, name, value);
}

// Constraints

char* get_constraint_name(void* constraintHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_getName(thread, constraintHandle);
}

void post(void* constraintHandle) {
    LAZY_THREAD_ATTACH
    Java_org_chocosolver_capi_ConstraintApi_post(thread, constraintHandle);
}

void* reify(void* constraintHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_reify(thread, constraintHandle);
}

int is_satisfied(void* constraintHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_is_satisfied(thread, constraintHandle);
}

void* arithm_iv_cst(void* modelHandle, void* intVarHandle, char* op, int constant) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_arithm_iv_cst(thread, modelHandle, intVarHandle, op, constant);
}

void* arithm_iv_iv(void* modelHandle, void* intVarHandle1, char* op, void* intVarHandle2) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_arithm_iv_iv(thread, modelHandle, intVarHandle1, op, intVarHandle2);
}

void* arithm_iv_iv_cst(void* modelHandle, void* intVarHandle1, char* op1, void* intVarHandle2, char* op2, int constant) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_arithm_iv_iv_cst(thread, modelHandle, intVarHandle1, op1, intVarHandle2, op1, constant);
}

void* arithm_iv_iv_iv(void* modelHandle, void* intVarHandle1, char* op1, void* intVarHandle2, char* op2, void* intVarHandle3) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_arithm_iv_iv_iv(thread, modelHandle, intVarHandle1, op1, intVarHandle2, op2, intVarHandle3);
}

void* member_iv_iarray(void* modelHandle, void* intVarHandle, void* tableHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_member_iv_iarray(thread, modelHandle, intVarHandle, tableHandle);
}

void* member_iv_i_i(void* modelHandle, void* intVarHandle, int lb, int ub) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_member_iv_i_i(thread, modelHandle, intVarHandle, lb, ub);
}

void* all_different(void* modelHandle, void* intVarArrayHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_allDifferent(thread, modelHandle, intVarArrayHandle);
}

void* mod_iv_i_i(void* modelHandle, void* intVarHandle, int mod, int result) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_mod_iv_i_i(thread, modelHandle, intVarHandle, mod, result);
}

void* mod_iv_i_iv(void* modelHandle, void* intVarHandle1, int mod, void* intVarHandle2) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_mod_iv_i_iv(thread, modelHandle, intVarHandle1, mod, intVarHandle2);
}

void* mod_iv_iv_iv(void* modelHandle, void* intVarHandle1, void* intVarHandle2, void* intVarHandle3) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_mod_iv_iv_iv(thread, modelHandle, intVarHandle1, intVarHandle2, intVarHandle3);
}

void* not(void* modelHandle, void* constraintHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_not(thread, modelHandle, constraintHandle);
}

void* not_member_iv_iarray(void* modelHandle, void* intVarHandle, void* tableHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_not_member_iv_iarray(thread, modelHandle, intVarHandle, tableHandle);
}

void* not_member_iv_i_i(void* modelHandle, void* intVarHandle, int lb, int ub) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_not_member_iv_i_i(thread, modelHandle, intVarHandle, lb, ub);
}

void* absolute(void* modelHandle, void* intVarHandle1, void* intVarHandle2) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_absolute(thread, modelHandle, intVarHandle1, intVarHandle2);
}

void* distance_iv_iv_i(void* modelHandle, void* intVarHandle1, void* intVarHandle2, char* op, int constant) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_distance_iv_iv_i(thread, modelHandle, intVarHandle1, intVarHandle2, op, constant);
}

void* distance_iv_iv_iv(void* modelHandle, void* intVarHandle1, void* intVarHandle2, char* op, void* intVarHandle3) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_distance_iv_iv_iv(thread, modelHandle, intVarHandle1, intVarHandle2, op, intVarHandle3);
}

void* element_iv_iarray_iv_i(void* modelHandle, void* intVarHandle1, void* tableHandle, void* intVarHandle2, int offset) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_element_iv_iarray_iv_i(thread, modelHandle, intVarHandle1, tableHandle, intVarHandle2, offset);
}

void* element_iv_ivarray_iv_i(void* modelHandle, void* intVarHandle1, void* intVarArrayHandle, void* intVarHandle2, int offset) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_element_iv_ivarray_iv_i(thread, modelHandle, intVarHandle1, intVarArrayHandle, intVarHandle2, offset);
}

void* square(void* modelHandle, void* intVarHandle1, void* intVarHandle2) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_square(thread, modelHandle, intVarHandle1, intVarHandle2);
}

void* times_iv_i_iv(void* modelHandle, void* intVarHandle1, int y, void* intVarHandle2) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_times_iv_i_iv(thread, modelHandle, intVarHandle1, y, intVarHandle2);
}

void* times_iv_iv_i(void* modelHandle, void* intVarHandle1, void* intVarHandle2, int z) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_times_iv_iv_i(thread, modelHandle, intVarHandle1, intVarHandle2, z);
}

void* times_iv_iv_iv(void* modelHandle, void* intVarHandle1, void* intVarHandle2, void* intVarHandle3) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_times_iv_iv_iv(thread, modelHandle, intVarHandle1, intVarHandle2, intVarHandle3);
}

void* div_(void* modelHandle, void* intVarHandle1, void* intVarHandle2, void* intVarHandle3) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_div(thread, modelHandle, intVarHandle1, intVarHandle2, intVarHandle3);
}

void* max_iv_iv_iv(void* modelHandle, void* intVarHandle1, void* intVarHandle2, void* intVarHandle3) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_max_iv_iv_iv(thread, modelHandle, intVarHandle1, intVarHandle2, intVarHandle3);
}

void* max_iv_ivarray(void* modelHandle, void* intVarHandle, void* intVarArrayHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_max_iv_ivarray(thread, modelHandle, intVarHandle, intVarArrayHandle);
}

void* min_iv_iv_iv(void* modelHandle, void* intVarHandle1, void* intVarHandle2, void* intVarHandle3) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_min_iv_iv_iv(thread, modelHandle, intVarHandle1, intVarHandle2, intVarHandle3);
}

void* min_iv_ivarray(void* modelHandle, void* intVarHandle, void* intVarArrayHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_min_iv_ivarray(thread, modelHandle, intVarHandle, intVarArrayHandle);
}

// Array API

// IntVar

void* create_intvar_array(int size) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ArrayApi_intVar_create(thread, size);
}

int intvar_array_length(void* arrayHande) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ArrayApi_intVar_length(thread, arrayHande);
}

void intvar_array_set(void* arrayHande, void* intVarHandle, int index) {
    LAZY_THREAD_ATTACH
    Java_org_chocosolver_capi_ArrayApi_intVar_set(thread, arrayHande, intVarHandle, index);
}

// int

void* create_int_array(int size) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ArrayApi_int_create(thread, size);
}

int int_array_length(void* intArrayHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ArrayApi_int_length(thread, intArrayHandle);
}

void int_array_set(void* intArrayHandle, int element, int index) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ArrayApi_int_set(thread, intArrayHandle, element, index);
}

// Criterion

void* create_criterion_array(int size) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ArrayApi_criterion_create(thread, size);
}

void criterion_array_set(void* criterionArrayHandle, void* criterionHandle, int index) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ArrayApi_criterion_set(thread, criterionArrayHandle, criterionHandle, index);
}

int array_length(void* arrayHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ArrayApi_length(thread, arrayHandle);
}

// List API

int list_size(void* listHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ListApi_size(thread, listHandle);
}

// Solution

void* list_solution_get(void* listHandle, int index) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ListApi_solution_get(thread, listHandle, index);
}

// Search

void set_random_search(void* solverHandle, void* intVarArrayHandle, long seed) {
    LAZY_THREAD_ATTACH
    Java_org_chocosolver_capi_SearchApi_set_random_search(thread, solverHandle, intVarArrayHandle, seed);
}

void set_dom_over_w_deg_search(void* solverHandle, void* intVarArrayHandle) {
    LAZY_THREAD_ATTACH
    Java_org_chocosolver_capi_SearchApi_set_dom_over_w_deg_search(thread, solverHandle, intVarArrayHandle);
}

void set_dom_over_w_deg_ref_search(void* solverHandle, void* intVarArrayHandle) {
    LAZY_THREAD_ATTACH
    Java_org_chocosolver_capi_SearchApi_set_dom_over_w_deg_ref_search(thread, solverHandle, intVarArrayHandle);
}

void set_activity_based_search(void* solverHandle, void* intVarArrayHandle) {
    LAZY_THREAD_ATTACH
    Java_org_chocosolver_capi_SearchApi_set_activity_based_search(thread, solverHandle, intVarArrayHandle);
}

void set_min_dom_lb_search(void* solverHandle, void* intVarArrayHandle) {
    LAZY_THREAD_ATTACH
    Java_org_chocosolver_capi_SearchApi_set_min_dom_lb_search(thread, solverHandle, intVarArrayHandle);
}

void set_min_dom_ub_search(void* solverHandle, void* intVarArrayHandle) {
    LAZY_THREAD_ATTACH
    Java_org_chocosolver_capi_SearchApi_set_min_dom_ub_search(thread, solverHandle, intVarArrayHandle);
}

void set_conflict_history_search(void* solverHandle, void* intVarArrayHandle) {
    LAZY_THREAD_ATTACH
    Java_org_chocosolver_capi_SearchApi_set_conflict_history_search(thread, solverHandle, intVarArrayHandle);
}

void set_default_search(void* solverHandle) {
    LAZY_THREAD_ATTACH
    Java_org_chocosolver_capi_SearchApi_set_default_search(thread, solverHandle);
}

void set_input_order_lb_search(void* solverHandle, void* intVarArrayHandle) {
    LAZY_THREAD_ATTACH
    Java_org_chocosolver_capi_SearchApi_set_input_order_lb_search(thread, solverHandle, intVarArrayHandle);
}

void set_input_order_ub_search(void* solverHandle, void* intVarArrayHandle) {
    LAZY_THREAD_ATTACH
    Java_org_chocosolver_capi_SearchApi_set_input_order_ub_search(thread, solverHandle, intVarArrayHandle);
}

void set_failure_length_based_search(void* solverHandle, void* intVarArrayHandle) {
    LAZY_THREAD_ATTACH
    Java_org_chocosolver_capi_SearchApi_set_failure_length_based_search(thread, solverHandle, intVarArrayHandle);
}

void set_failure_rate_based_search(void* solverHandle, void* intVarArrayHandle) {
    LAZY_THREAD_ATTACH
    Java_org_chocosolver_capi_SearchApi_set_failure_rate_based_search(thread, solverHandle, intVarArrayHandle);
}

// Handle API

void chocosolver_handles_destroy(void* handle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_HandlesApi_destroy(thread, handle);
}

