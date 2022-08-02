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

void* get_solver(void*);

// Solver API

void* find_solution(void*, void*);

void* find_all_solutions(void*, void*);

void* find_optimal_solution(void*, void*, _Bool, void*);

void* find_all_optimal_solutions(void*, void*, _Bool, void*);

void show_statistics(void*);

void show_short_statistics(void*);

// Solution API

int get_int_val(void*, void*);

// Criterion API

void* time_counter(void*, long);

void* solution_counter(void*, long);

void* node_counter(void*, long);

void* fail_counter(void*, long);

void* restart_counter(void*, long);

void* backtrack_counter(void*, long);

// Intvars

void* intvar_sii(void*, char*, int, int);

void* intvar_ii(void*, int, int);

char* get_intvar_name(void*);

int get_intvar_lb(void*);

int get_intvar_ub(void*);

// Boolvars

void* boolvar_s(void*, char*);

void* boolvar(void*);

void* boolvar_b(void*, _Bool);

void* boolvar_sb(void*, char*, _Bool);

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

// Array API

// IntVar

void* create_intvar_array(int);

int intvar_array_length(void*);

void intvar_array_set(void*, void*, int);

// int

void* create_int_array(int);

int int_array_length(void*);

void int_array_set(void*, int, int);

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

// Handle API

void chocosolver_handles_destroy(void*);

#if defined(__cplusplus)
}
#endif
#endif