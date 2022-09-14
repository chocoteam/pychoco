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

void* create_model_s(char* name) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ModelApi_createModel_s(thread, name);
}

void* create_model() {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ModelApi_createModel(thread);
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

int solve(void* solverHandle, void* stopArrayHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_SolverApi_solve(thread, solverHandle, stopArrayHandle);
}

void* find_solution(void* solverHandle, void* stopArrayHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_SolverApi_findSolution(thread, solverHandle, stopArrayHandle);
}

void* find_all_solutions(void* solverHandle, void* stopArrayHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_SolverApi_findAllSolutions(thread, solverHandle, stopArrayHandle);
}

void* find_optimal_solution(void* solverHandle, void* objectiveVarHandle, int maximize, void* stop) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_SolverApi_findOptimalSolution(thread, solverHandle, objectiveVarHandle, maximize, stop);
}

void* find_all_optimal_solutions(void* solverHandle, void* objectiveVarHandle, int maximize, void* stop) {
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

long get_solution_count(void* solverHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_SolverApi_getSolutionCount(thread, solverHandle);
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

// Variable (generic)

char* get_variable_name(void* varHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_VariableApi_getName(thread, varHandle);
}

int is_instantiated(void* varHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_VariableApi_isInstantiated(thread, varHandle);
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

void* intvar_i(void* modelHandle, int value) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_IntVarApi_intVar_i(thread, modelHandle, value);
}

void* intvar_si(void* modelHandle, char* name, int value) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_IntVarApi_intVar_si(thread, modelHandle, name, value);
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

int get_intvar_value(void* varHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_IntVarApi_getValue(thread, varHandle);
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

void* boolvar_b(void* modelHandle, int value) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_BoolVarApi_boolVar_b(thread, modelHandle, value);
}

void* boolvar_sb(void* modelHandle, char* name, int value) {
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
    return Java_org_chocosolver_capi_ConstraintApi_arithm_iv_iv_cst(thread, modelHandle, intVarHandle1, op1, intVarHandle2, op2, constant);
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

void* not_(void* modelHandle, void* constraintHandle) {
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

void* table(void* modelHandle, void* varsHandle, void* tuplesHandle, int feasible, char* algo) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_table(thread, modelHandle, varsHandle, tuplesHandle, feasible, algo);
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

void* pow_(void* modelHandle, void* intVarHandle1, int c, void* intVarHandle2) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_pow(thread, modelHandle, intVarHandle1, c, intVarHandle2);
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

void* all_equal(void* modelHandle, void* intVarArrayHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_all_equal(thread, modelHandle, intVarArrayHandle);
}

void* not_all_equal(void* modelHandle, void* intVarArrayHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_not_all_equal(thread, modelHandle, intVarArrayHandle);
}

void* among(void* modelHandle, void* nbVarHandle, void* intVarArrayHandle, void* valuesHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_among(thread, modelHandle, nbVarHandle,
                                                         intVarArrayHandle, valuesHandle);
}

void* and_bv_bv(void* modelHandle, void* boolVarArrayHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_and_bv_bv(thread, modelHandle, boolVarArrayHandle);
}

void* and_cs_cs(void* modelHandle, void* constraintArrayHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_and_cs_cs(thread, modelHandle, constraintArrayHandle);
}

void* at_least_n_values(void* modelHandle, void* intVarArrayHandle, void* nValuesHandle, int AC) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_atLeastNValues(
        thread,
        modelHandle,
        intVarArrayHandle,
        nValuesHandle,
        AC
    );
}

void* at_most_n_values(void* modelHandle, void* intVarArrayHandle, void* nValuesHandle, int STRONG) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_atMostNValues(
        thread,
        modelHandle,
        intVarArrayHandle,
        nValuesHandle,
        STRONG
    );
}

void* bin_packing(void* modelHandle, void* itemBinHandle, void* itemSizeHandle, void* binLoadHandle, int offset) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_binPacking(
        thread,
        modelHandle,
        itemBinHandle,
        itemSizeHandle,
        binLoadHandle,
        offset
    );
}

void* bools_int_channeling(void* modelHandle, void* boolVarArrayHandle, void* intVarHandle, int offset) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_boolsIntChanneling(
        thread,
        modelHandle,
        boolVarArrayHandle,
        intVarHandle,
        offset
    );
}

void* bits_int_channeling(void* modelHandle, void* boolVarArrayHandle, void* intVarHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_bitsIntChanneling(
        thread,
        modelHandle,
        boolVarArrayHandle,
        intVarHandle
    );
}

void* clauses_int_channeling(void* modelHandle, void* intVarHandle, void* eVarsHandle, void* lVarsHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_clausesIntChanneling(
        thread,
        modelHandle,
        intVarHandle,
        eVarsHandle,
        lVarsHandle
    );
}

void* circuit(void* modelHandle, void* intVarArrayHandle, int offset, char* conf) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_circuit(
        thread,
        modelHandle,
        intVarArrayHandle,
        offset,
        conf
    );
}

void* cost_regular(void* modelHandle, void* intVarsHandle, void* costHandle, void* costAutomatonHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_cost_regular(
        thread,
        modelHandle,
        intVarsHandle,
        costHandle,costAutomatonHandle
    );
}

void* count_i(void* modelHandle, int value, void* intVarArrayHandle, void* limitHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_count_i(
        thread,
        modelHandle,
        value,
        intVarArrayHandle,
        limitHandle
    );
}

void* count_iv(void* modelHandle, void* valueHandle, void* intVarArrayHandle, void* limitHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_count_iv(
        thread,
        modelHandle,
        valueHandle,
        intVarArrayHandle,
        limitHandle
    );
}

void* cumulative(void* modelHandle, void* tasksHandle, void* heightsHandle, void* capacityHandle, int incr) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_cumulative(
        thread,
        modelHandle,
        tasksHandle,
        heightsHandle,
        capacityHandle,
        incr
    );
}

void* diff_n(void* modelHandle, void* XHandle, void* YHandle, void* widthHandle, void* heightHandle,
             int addCumulativeReasoning) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_diffN(
        thread,
        modelHandle,
        XHandle,
        YHandle,
        widthHandle,
        heightHandle,
        addCumulativeReasoning
    );
}

void* decreasing(void* modelHandle, void* intVarArrayHandle, int delta) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_decreasing(thread, modelHandle, intVarArrayHandle, delta);
}

void* increasing(void* modelHandle, void* intVarArrayHandle, int delta) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_increasing(thread, modelHandle, intVarArrayHandle, delta);
}

void* global_cardinality(void* modelHandle, void* intVarArrayHandle, void* valuesHandle,
                         void* occurrencesHandle, int closed) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_globalCardinality(
        thread,
        modelHandle,
        intVarArrayHandle,
        valuesHandle,
        occurrencesHandle,
        closed
    );
}

void* inverse_channeling(void* modelHandle, void* intVarArrayHandle1, void* intVarArrayHandle2,
                         int offset1, int offset2, int ac) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_inverseChanneling(
        thread,
        modelHandle,
        intVarArrayHandle1,
        intVarArrayHandle2,
        offset1,
        offset2,
        ac
    );
}

void* int_value_precede_chain(void* modelHandle, void* intVarsHandle, void* VHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_intValuePrecedeChain(
        thread,
        modelHandle,
        intVarsHandle,
        VHandle
    );
}

void* keysort(void* modelHandle, void* varsHandle, void* permVarsHandle, void* sortedVarsHandle, int k) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_keysort(
        thread,
        modelHandle,
        varsHandle,
        permVarsHandle,
        sortedVarsHandle,
        k
    );
}

void* knapsack(void* modelHandle, void* occurrencesHandle, void* weightSumHandle, void* energySumHandle,
               void* weightHandle, void* energyHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_knapsack(
        thread,
        modelHandle,
        occurrencesHandle,
        weightSumHandle,
        energySumHandle,
        weightHandle,
        energyHandle
    );
}

void* lex_chain_less(void* modelHandle, void* intVarsHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_lexChainLess(
        thread,
        modelHandle,
        intVarsHandle
    );
}

void* lex_chain_less_eq(void* modelHandle, void* intVarsHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_lexChainLessEq(
        thread,
        modelHandle,
        intVarsHandle
    );
}

void* lex_less(void* modelHandle, void* intVarsHandle1, void* intVarsHandle2) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_lexLess(
        thread,
        modelHandle,
        intVarsHandle1,
        intVarsHandle2
    );
}

void* lex_less_eq(void* modelHandle, void* intVarsHandle1, void* intVarsHandle2) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_lexLessEq(
        thread,
        modelHandle,
        intVarsHandle1,
        intVarsHandle2
    );
}

void* argmax(void* modelHandle, void* intVarHandle, int offset, void* intVarsHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_argmax(
        thread,
        modelHandle,
        intVarHandle,
        offset,
        intVarsHandle
    );
}

void* argmin(void* modelHandle, void* intVarHandle, int offset, void* intVarsHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_argmin(
        thread,
        modelHandle,
        intVarHandle,
        offset,
        intVarsHandle
    );
}

void* n_values(void* modelHandle, void* intVarsHandle, void* nValuesHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_nValues(
        thread,
        modelHandle,
        intVarsHandle,
        nValuesHandle
    );
}

void* or_bv_bv(void* modelHandle, void* boolVarArrayHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_or_bv_bv(thread, modelHandle, boolVarArrayHandle);
}

void* or_cs_cs(void* modelHandle, void* constraintArrayHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_or_cs_cs(thread, modelHandle, constraintArrayHandle);
}

void* path(void* modelHandle, void* intVarsHandle, void* startHandle, void* endHandle, int offset) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_path(
        thread,
        modelHandle,
        intVarsHandle,
        startHandle,
        endHandle,
        offset
    );
}

void* regular(void* modelHandle, void* intVarsHandle, void* automatonHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_regular(
        thread,
        modelHandle,
        intVarsHandle,
        automatonHandle
    );
}

void* scalar_i(void* modelHandle, void* intVarsHandle, void* coeffsHandle, char* op, int scalar) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_scalar_i(
        thread,
        modelHandle,
        intVarsHandle,
        coeffsHandle,
        op,
        scalar
    );
}

void* scalar_iv(void* modelHandle, void* intVarsHandle, void* coeffsHandle, char* op, void* scalarHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_scalar_iv(
        thread,
        modelHandle,
        intVarsHandle,
        coeffsHandle,
        op,
        scalarHandle
    );
}

void* sort(void* modelHandle, void* intVarsHandle, void* sortedIntVarsHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_sort(
        thread,
        modelHandle,
        intVarsHandle,
        sortedIntVarsHandle
    );
}

void* sub_circuit(void* modelHandle, void* intVarsHandle, int offset, void* subCircuitLengthHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_subCircuit(
        thread,
        modelHandle,
        intVarsHandle,
        offset,
        subCircuitLengthHandle
    );
}

void* sub_path(void* modelHandle, void* intVarsHandle, void* startHandle, void* endHandle, int offset, void* lengthHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_subPath(
        thread,
        modelHandle,
        intVarsHandle,
        startHandle,
        endHandle,
        offset,
        lengthHandle
    );
}

void* sum_iv_i(void* modelHandle, void* intVarsHandle, char* op, int sum) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_sum_iv_i(
        thread,
        modelHandle,
        intVarsHandle,
        op,
        sum
    );
}

void* sum_iv_iv(void* modelHandle, void* intVarsHandle, char* op, void* sumHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_sum_iv_iv(
        thread,
        modelHandle,
        intVarsHandle,
        op,
        sumHandle
    );
}

void* sum_ivarray_ivarray(void* modelHandle, void* intVarsHandle1, char* op, void* intVarsHandle2) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_sum_ivarray_ivarray(
        thread,
        modelHandle,
        intVarsHandle1,
        op,
        intVarsHandle2
    );
}

void* sum_bv_i(void* modelHandle, void* boolVarsHandle, char* op, int sum) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_sum_bv_i(
        thread,
        modelHandle,
        boolVarsHandle,
        op,
        sum
    );
}

void* sum_bv_iv(void* modelHandle, void* boolVarsHandle, char* op, void* sumHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_sum_bv_iv(
        thread,
        modelHandle,
        boolVarsHandle,
        op,
        sumHandle
    );
}

void* tree(void* modelHandle, void* successorsHandle, void* nbTreeHandle , int offset) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ConstraintApi_tree(
        thread,
        modelHandle,
        successorsHandle,
        nbTreeHandle,
        offset
    );
}

// Array API

// IntVar

void* create_intvar_array(int size) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ArrayApi_intVar_create(thread, size);
}

int intvar_array_length(void* arrayHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ArrayApi_intVar_length(thread, arrayHandle);
}

void intvar_array_set(void* arrayHandle, void* intVarHandle, int index) {
    LAZY_THREAD_ATTACH
    Java_org_chocosolver_capi_ArrayApi_intVar_set(thread, arrayHandle, intVarHandle, index);
}

// IntVar[][]

void* create_intvar_array_array(int size) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ArrayApi_intVar_array_create(thread, size);
}

int intvar_array_array_length(void* arrayHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ArrayApi_intVar_array_length(thread, arrayHandle);
}

void intvar_array_array_set(void* arrayHandle, void* intVarArrayHandle, int index) {
    LAZY_THREAD_ATTACH
    Java_org_chocosolver_capi_ArrayApi_intVar_array_set(thread, arrayHandle, intVarArrayHandle, index);
}
// Tasks

void* create_task_array(int size) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ArrayApi_task_create(thread, size);
}

int task_array_length(void* arrayHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ArrayApi_task_length(thread, arrayHandle);
}

void task_array_set(void* arrayHandle, void* elementHandle, int index) {
    LAZY_THREAD_ATTACH
    Java_org_chocosolver_capi_ArrayApi_task_set(thread, arrayHandle, elementHandle, index);
}


// BoolVar

void* create_boolvar_array(int size) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ArrayApi_boolVar_create(thread, size);
}

void boolvar_array_set(void* arrayHandle, void* boolVarHandle, int index) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ArrayApi_boolVar_set(thread, arrayHandle, boolVarHandle, index);
}

// Constraint

void* create_constraint_array(int size) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ArrayApi_constraint_create(thread, size);
}

void constraint_array_set(void* arrayHandle, void* constraintHandle, int index) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ArrayApi_constraint_set(thread, arrayHandle, constraintHandle, index);
}

// int[]

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

// int[][]

void* create_int_array_array(int size) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ArrayApi_int_array_create(thread, size);
}

int int_array_array_length(void* arrayHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ArrayApi_int_array_length(thread, arrayHandle);
}

void int_array_array_set(void* arrayHandle, void* elementHandle, int index) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ArrayApi_int_array_set(thread, arrayHandle, elementHandle, index);
}

// int[][][]

void* create_int_array_array_array(int size) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ArrayApi_int_array_array_create(thread, size);
}

int int_array_array_array_length(void* arrayHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ArrayApi_int_array_array_length(thread, arrayHandle);
}

void int_array_array_array_set(void* arrayHandle, void* elementHandle, int index) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_ArrayApi_int_array_array_set(thread, arrayHandle, elementHandle, index);
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

// Automaton API

void* create_fa() {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_AutomatonApi_create_fa(thread);
}

void* create_fa_regexp(char* regexp) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_AutomatonApi_create_fa_regexp(thread, regexp);
}

void* create_fa_regexp_min_max(char* regexp, int min, int max) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_AutomatonApi_create_fa_regexp_min_max(thread, regexp, min, max);
}

void* create_cost_fa() {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_AutomatonApi_create_cost_fa(thread);
}

void* create_cost_fa_from_fa(void* faHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_AutomatonApi_create_cost_fa_from_automaton(thread, faHandle);
}

int get_nb_states(void* faHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_AutomatonApi_get_nb_states(thread, faHandle);
}

int get_nb_symbols(void* faHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_AutomatonApi_get_nb_symbols(thread, faHandle);
}

int add_state(void* faHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_AutomatonApi_add_state(thread, faHandle);
}

void remove_symbol(void* faHandle, int symbol) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_AutomatonApi_remove_symbol(thread, faHandle, symbol);
}

void add_transition(void* faHandle, int source, int destination, void* symbolsHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_AutomatonApi_add_transition(thread, faHandle, source, destination, symbolsHandle);
}

void delete_transition(void* faHandle, int source, int destination, int symbol) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_AutomatonApi_delete_transition(thread, faHandle, source, destination, symbol);
}

int get_initial_state(void* faHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_AutomatonApi_get_initial_state(thread, faHandle);
}

int is_final(void* faHandle, int state) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_AutomatonApi_is_final(thread, faHandle, state);
}

void set_initial_state(void* faHandle, int state) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_AutomatonApi_set_initial_state(thread, faHandle, state);
}

void set_final(void* faHandle, void* statesHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_AutomatonApi_set_final(thread, faHandle, statesHandle);
}

void set_non_final(void* faHandle, void* statesHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_AutomatonApi_set_non_final(thread, faHandle, statesHandle);
}

void cost_fa_add_counter(void* costFaHandle, void* counterHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_AutomatonApi_cost_fa_add_counter(thread, costFaHandle, counterHandle);
}

void* fa_union(void* faHandle, void* otherFaHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_AutomatonApi_union(thread, faHandle, otherFaHandle);
}

void fa_minimize(void* faHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_AutomatonApi_minimize(thread, faHandle);
}

void* fa_complement(void* faHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_AutomatonApi_complement(thread, faHandle);
}

void* create_counter_state(void* layerValueStateHandle, int min, int max) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_AutomatonApi_create_counter_state(thread, layerValueStateHandle, min, max);
}

void* make_single_resource_ii(void* automatonHandle, void* costsHandle, int inf, int sup) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_AutomatonApi_make_single_resource_ii(thread, automatonHandle, costsHandle, inf, sup);
}

void* make_single_resource_iii(void* automatonHandle, void* costsHandle, int inf, int sup) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_AutomatonApi_make_single_resource_iii(thread, automatonHandle, costsHandle, inf, sup);
}

// Task API

void* create_task_iv_i(void* startHandle, int d) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_TaskApi_create_iv_i(thread, startHandle, d);
}

void* create_task_iv_i_iv(void* startHandle, int d, void* endHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_TaskApi_create_iv_i_iv(thread, startHandle, d, endHandle);
}

void* create_task_iv_iv_iv(void* startHandle, void* durationHandle, void* endHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_TaskApi_create_iv_iv_iv(thread, startHandle, durationHandle, endHandle);
}

void task_ensure_bound_consistency(void* taskHandle) {
    LAZY_THREAD_ATTACH
    Java_org_chocosolver_capi_TaskApi_ensure_bound_consistency(thread, taskHandle);
}

void* task_get_start(void* taskHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_TaskApi_get_start(thread, taskHandle);

}

void* task_get_end(void* taskHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_TaskApi_get_end(thread, taskHandle);
}

void* task_get_duration(void* taskHandle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_TaskApi_get_duration(thread, taskHandle);
}

// Handle API

void chocosolver_handles_destroy(void* handle) {
    LAZY_THREAD_ATTACH
    return Java_org_chocosolver_capi_HandlesApi_destroy(thread, handle);
}

