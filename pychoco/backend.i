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

void* create_model();
void* create_model_s(char*);
char* get_model_name(void*);
void* get_solver(void*);

// Solver API

int solve(void*, void*);
void* find_solution(void*, void*);
void* find_all_solutions(void*, void*);
void* find_optimal_solution(void*, void*, int, void*);
void* find_all_optimal_solutions(void*, void*, int, void*);
void show_statistics(void*);
void show_short_statistics(void*);
long get_solution_count(void*);

// Criterion API

void* time_counter(void*, long);
void* solution_counter(void*, long);
void* node_counter(void*, long);
void* fail_counter(void*, long);
void* restart_counter(void*, long);
void* backtrack_counter(void*, long);

// Solution API

int get_int_val(void*, void*);

// Variable (generic)

char* get_variable_name(void*);
int is_instantiated(void*);
int is_view(void*);

// Intvars

void* intvar_sii(void*, char*, int, int);
void* intvar_ii(void*, int, int);
void* intvar_i(void*, int);
void* intvar_si(void*, char*, int);
char* get_intvar_name(void*);
int get_intvar_lb(void*);
int get_intvar_ub(void*);
int get_intvar_value(void*);

// Boolvars

void* boolvar_s(void*, char*);
void* boolvar(void*);
void* boolvar_b(void*, int);
void* boolvar_sb(void*, char*, int);

// SetVars

void* setvar_s_iviv(void*, char*, void*, void*);
void* setvar_iviv(void*, void*, void*);
void* setvar_s_iv(void*, char*, void*);
void* setvar_iv(void*, void*);
void* get_setvar_lb(void*);
void* get_setvar_ub(void*);
void* get_setvar_value(void*);

// GraphVars

void* create_graphvar(void*, char*, void*, void*);
void* create_digraphvar(void*, char*, void*, void*);
void* create_node_induced_graphvar(void*, char*, void*, void*);
void* create_node_induced_digraphvar(void*, char*, void*, void*);
void* get_graphvar_lb(void*);
void* get_graphvar_ub(void*);
void* get_graphvar_value(void*);

// Constraints

char* get_constraint_name(void*);
void post(void*);
void* reify(void*);
int is_satisfied(void*);

// IntVar and BoolVar constraints

void* arithm_iv_cst(void*, void*, char*, int);
void* arithm_iv_iv(void*, void*, char*, void*);
void* arithm_iv_iv_cst(void*, void*, char*, void*, char*, int);
void* arithm_iv_iv_iv(void*, void*, char*, void*, char*, void*);
void* member_iv_iarray(void*, void*, void*);
void* member_iv_i_i(void*, void*, int, int);
void* mod_iv_i_i(void*, void*, int, int);
void* mod_iv_i_iv(void*, void*, int, void*);
void* mod_iv_iv_iv(void*, void*, void*, void*);
void* not_(void*, void*);
void* not_member_iv_iarray(void*, void*, void*);
void* not_member_iv_i_i(void*, void*, int, int);
void* absolute(void*, void*, void*);
void* distance_iv_iv_i(void*, void*, void*, char*, int);
void* distance_iv_iv_iv(void*, void*, void*, char*, void*);
void* element_iv_iarray_iv_i(void*, void*, void*, void*, int);
void* element_iv_ivarray_iv_i(void*, void*, void*, void*, int);
void* square(void*, void*, void*);
void* table(void*, void*, void*, int, char*);
void* times_iv_i_iv(void*, void*, int, void*);
void* times_iv_iv_i(void*, void*, void*, int);
void* times_iv_iv_iv(void*, void*, void*, void*);
void* pow_(void*, void*, int, void*);
void* div_(void*, void*, void*, void*);
void* max_iv_iv_iv(void*, void*, void*, void*);
void* max_iv_ivarray(void*, void*, void*);
void* mddc(void*, void*, void*);
void* min_iv_iv_iv(void*, void*, void*, void*);
void* min_iv_ivarray(void*, void*, void*);
void* multi_cost_regular(void*, void*, void*, void*);
void* all_different(void*, void*);
void* all_different_except_0(void*, void*);
void* all_different_prec_pred_succ(void*, void*, void*, void*);
void* all_different_prec_prec(void*, void*, void*);
void* all_equal(void*, void*);
void* not_all_equal(void*, void*);
void* among(void*, void*, void*, void*);
void* and_bv_bv(void*, void*);
void* and_cs_cs(void*, void*);
void* at_least_n_values(void*, void*, void*, int);
void* at_most_n_values(void*, void*, void*, int);
void* bin_packing(void*, void*, void*, void*, int);
void* bools_int_channeling(void*, void*, void*, int);
void* bits_int_channeling(void*, void*, void*);
void* clauses_int_channeling(void*, void*, void*, void*);
void* circuit(void*, void*, int, char*);
void* cost_regular(void*, void*, void*, void*);
void* count_i(void*, int, void*, void*);
void* count_iv(void*, void*, void*, void*);
void* cumulative(void*, void*, void*, void*, int);
void* diff_n(void*, void*, void*, void*, void*, int);
void* decreasing(void*, void*, int);
void* increasing(void*, void*, int);
void* global_cardinality(void*, void*, void*, void*, int);
void* inverse_channeling(void*, void*, void*, int, int, int);
void* int_value_precede_chain(void*, void*, void*);
void* keysort(void*, void*, void*, void*, int);
void* knapsack(void*, void*, void*, void*, void*, void*);
void* lex_chain_less(void*, void*);
void* lex_chain_less_eq(void*, void*);
void* lex_less(void*, void*, void*);
void* lex_less_eq(void*, void*, void*);
void* argmax(void*, void*, int, void*);
void* argmin(void*, void*, int, void*);
void* n_values(void*, void*, void*);
void* or_bv_bv(void*, void*);
void* or_cs_cs(void*, void*);
void* path(void*, void*, void*, void*, int);
void* regular(void*, void*, void*);
void* scalar_i(void*, void*, void*, char*, int);
void* scalar_iv(void*, void*, void*, char*, void*);
void* sort(void*, void*, void*);
void* sub_circuit(void*, void*, int, void*);
void* sub_path(void*, void*, void*, void*, int, void*);
void* sum_iv_i(void*, void*, char*, int);
void* sum_iv_iv(void*, void*, char*, void*);
void* sum_ivarray_ivarray(void*, void*, char*, void*);
void* sum_bv_i(void*, void*, char*, int);
void* sum_bv_iv(void*, void*, char*, void*);
void* tree(void*, void*, void*, int);

// SetVar constraints

void* set_union_ints(void*, void*, void*);
void* set_union(void*, void*, void*);
void* set_union_indices(void*, void*, void*, void*, int, int);
void* set_intersection(void*, void*, void*, int);
void* set_subset_eq(void*, void*);
void* set_nb_empty(void*, void*, void*);
void* set_offset(void*, void*, void*, int);
void* set_not_empty(void*, void*);
void* set_sum(void*, void*, void*);
void* set_sum_elements(void*, void*, void*, int, void*);
void* set_max(void*, void*, void*, int);
void* set_max_indices(void*, void*, void*, int, void*, int);
void* set_min(void*, void*, void*, int);
void* set_min_indices(void*, void*, void*, int, void*, int);
void* set_bools_channeling(void*, void*, void*, int);
void* set_ints_channeling(void*, void*, void*, int, int);
void* set_disjoint(void*, void*, void*);
void* set_all_disjoint(void*, void*);
void* set_all_different(void*, void*);
void* set_all_equal(void*, void*);
void* set_partition(void*, void*, void*);
void* set_inverse_set(void*, void*, void*, int, int);
void* set_symmetric(void*, void*, int);
void* set_element(void*, void*, void*, int, void*);
void* set_member_set(void*, void*, void*);
void* set_member_int(void*, void*, void*);
void* set_not_member_int(void*, void*, void*);
void* set_le(void*, void*, void*);
void* set_lt(void*, void*, void*);

// View API

void* bool_not_view(void*);
void* set_bool_view(void*, int);
void* set_bools_view(void*, int, int);

void* int_offset_view(void*, int);
void* int_minus_view(void*);
void* int_scale_view(void*, int);
void* int_abs_view(void*);
void* int_affine_view(int, void*, int);
void* int_eq_view(void*, int);
void* int_ne_view(void*, int);
void* int_le_view(void*, int);
void* int_ge_view(void*, int);

void* bools_set_view(void*, int);
void* ints_set_view(void*, void*, int);
void* set_union_view(void*);
void* set_intersection_view(void*);
void* set_difference_view(void*, void*);

// Array API

// IntVar

void* create_intvar_array(int);
int intvar_array_length(void*);
void intvar_array_set(void*, void*, int);
void* intvar_array_get(void*, int);

// IntVar[][]

void* create_intvar_2d_array(int);
int intvar_2d_array_length(void*);
void intvar_2d_array_set(void*, void*, int);

// Tasks

void* create_task_array(int);
int task_array_length(void*);
void task_array_set(void*, void*, int);

// BoolVar

void* create_boolvar_array(int);
void boolvar_array_set(void*, void*, int);

// SetVar

void* create_setvar_array(int);
int setvar_array_length(void*);
void setvar_array_set(void*, void*, int);


// Constraint

void* create_constraint_array(int);
void constraint_array_set(void*, void*, int);

// int[]

void* create_int_array(int);
int int_array_length(void*);
void int_array_set(void*, int, int);
int int_array_get(void*, int);

// int[][]

void* create_int_2d_array(int);
int int_2d_array_length(void*);
void int_2d_array_set(void*, void*, int);

// int[][][]

void* create_int_3d_array(int);
int int_3d_array_length(void*);
void int_3d_array_set(void*, void*, int);

// int[][][][]

void* create_int_4d_array(int);
int int_4d_array_length(void*);
void int_4d_array_set(void*, void*, int);

// Criterion

void* create_criterion_array(int);
void criterion_array_set(void*, void*, int);
int array_length(void*);

// List API

int list_size(void*);

// Solution

void* list_solution_get(void*, int);

// Search

void set_random_search(void*, void*, long);
void set_dom_over_w_deg_search(void*, void*);
void set_dom_over_w_deg_ref_search(void*, void*);
void set_activity_based_search(void*, void*);
void set_min_dom_lb_search(void*, void*);
void set_min_dom_ub_search(void*, void*);
void set_conflict_history_search(void*, void*);
void set_default_search(void*);
void set_input_order_lb_search(void*, void*);
void set_input_order_ub_search(void*, void*);
void set_failure_length_based_search(void*, void*);
void set_failure_rate_based_search(void*, void*);

// Automaton API

void* create_fa();
void* create_fa_regexp(char*);
void* create_fa_regexp_min_max(char*, int, int);
void* create_cost_fa();
void* create_cost_fa_from_fa(void*);
int get_nb_states(void*);
int get_nb_symbols(void*);
int add_state(void*);
void remove_symbol(void*, int);
void add_transition(void*, int, int, void*);
void delete_transition(void*, int, int, int);
int get_initial_state(void*);
int is_final(void*, int);
void set_initial_state(void*, int);
void set_final(void*, void*);
void set_non_final(void*, void*);
void cost_fa_add_counter(void*, void*);
void* fa_union(void*, void*);
void fa_minimize(void*);
void* fa_complement(void*);
void* create_counter_state(void*, int, int);
void* make_single_resource_ii(void*, void*, int, int);
void* make_single_resource_iii(void*, void*, int, int);
void* make_multi_resources_iii(void*, void*, void*);
void* make_multi_resources_iiii(void*, void*, void*);

// Task API

void* create_task_iv_i(void*, int);
void* create_task_iv_i_iv(void*, int, void*);
void* create_task_iv_iv_iv(void*, void*, void*);
void task_ensure_bound_consistency(void*);
void* task_get_start(void*);
void* task_get_end(void*);
void* task_get_duration(void*);

// MDD API

void* create_mdd_tuples(void*, void*, int, int);
void* create_mdd_transitions(void*, void*);

// Graph API

void* create_graph(void*, int, char*, char*, int);
void* create_digraph(void*, int, char*, char*, int);

void* get_nodes(void*);
int add_node(void*, int);
int remove_node(void*, int);
int add_edge(void*, int, int);
int remove_edge(void*, int, int);
int get_nb_max_nodes(void*);
char* get_node_set_type(void*);
char* get_edge_set_type(void*);
int contains_node(void*, int);
int contains_edge(void*, int, int);
int is_directed(void*);
void* get_successors_of(void*, int);
void* get_predecessors_of(void*, int);
char* graphviz_export(void*);

// Handle API

void chocosolver_handles_destroy(void*);
