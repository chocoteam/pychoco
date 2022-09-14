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

// Solution API

int get_int_val(void*, void*);

// Criterion API

void* time_counter(void*, long);

void* solution_counter(void*, long);

void* node_counter(void*, long);

void* fail_counter(void*, long);

void* restart_counter(void*, long);

void* backtrack_counter(void*, long);

// Variable (generic)

char* get_variable_name(void*);

int is_instantiated(void*);

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

// Constraints

char* get_constraint_name(void*);

void post(void*);

void* reify(void*);

int is_satisfied(void*);

void* arithm_iv_cst(void*, void*, char*, int);

void* arithm_iv_iv(void*, void*, char*, void*);

void* arithm_iv_iv_cst(void*, void*, char*, void*, char*, int);

void* arithm_iv_iv_iv(void*, void*, char*, void*, char*, void*);

void* member_iv_iarray(void*, void*, void*);

void* member_iv_i_i(void*, void*, int, int);

void* all_different(void*, void*);

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

// Array API

// IntVar

void* create_intvar_array(int);

int intvar_array_length(void*);

void intvar_array_set(void*, void*, int);

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

// Constraint

void* create_constraint_array(int);

void constraint_array_set(void*, void*, int);

// int[]

void* create_int_array(int);

int int_array_length(void*);

void int_array_set(void*, int, int);

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

// Handle API

void chocosolver_handles_destroy(void*);

#if defined(__cplusplus)
}
#endif
#endif