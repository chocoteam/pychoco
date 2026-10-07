# pychoco 0.4.0

- Update to choco-solver 6.0.2
- Add custom constraints defined in Python: `model.custom_constraint(intvars, propagate_fn, is_entailed_fn, priority)`
  or by subclassing `Propagator`
- Add filtering methods on intvars, to be used in custom propagators: `update_lb`, `update_ub`, `instantiate_to`
  and `remove_value`
- Add custom search strategies defined in Python: `solver.set_custom_search(intvars, var_selector, val_selector)`
- Add backtrackable state objects: `model.make_state_int()` and `model.make_state_bool()`
- Add `algo` option in `all_different`
- Add `consistency` option in `global_cardinality` ("DEFAULT", "BC" or "AC"), bound-consistency is now the default

# pychoco 0.3.0

- Update to choco-solver 6.0.0
- Require Python >= 3.10
- Add solver settings as `Model` arguments (`lcg`, `enable_sat`, `table_substitution`, `max_learnt_clauses`...),
  which gives access to Lazy Clause Generation with `Model(lcg=True)`
- Add hints in solver: `add_hint` and `rem_hints`
- Add restart policies in solver: `set_luby_restart`, `set_geometrical_restart` and `set_restart_on_solutions`
- Add nogood recording in solver: `set_nogood_recording_from_restarts` and `set_nogood_recording_from_solutions`
- Add `show_decisions` and `show_solutions` in solver
- Add `set_round_robin_search` search strategy, remove `set_pick_on_fil_search`
- Add `uvalue` option in `MultivaluedDecisionDiagram`
- Add `unalterable` option in `ParallelPortfolio.add_model`, remove the `search_auto_conf` option of `ParallelPortfolio`
- `table` constraint now uses the `CT+` algorithm by default
- Remove the `incremental` option of `cumulative`
- Remove `Task.ensure_bound_consistency`

# pychoco 0.2.5 - 0.2.6

- Nothing new, just compile wheels for Python 3.14 

# pychoco 0.2.4

- Update to choco-solver 4.10.18
- Add JOSS paper

# pychoco 0.2.3

Rename `handle` property to `_handle` to avoid including it in autocompletion for IDE users.
Also introduce minor fixes.

# pychoco 0.2.2

Add accessors to solver statistics:

- `get_time_count()`
- `get_node_count()`
- `get_backtrack_count()`
- `get_fail_count()`
- `get_restart_count()`
- `is_objective_optimal()`
- `get_search_state()`

# pychoco 0.2.1

Same as 0.2.0 but fixing a wheel distribution issue.

# pychoco 0.2.0

- Update to choco-solver 4.10.16
- Add `bounded_domain` option in intvar
- Add reification constraints
- Add `pick_on_dom` and `pick_on_fil` search strategies
- Add `show_restarts` in solver
- Add hybrid table constraint
- Add universal value in table constraint
- Add 2D shape intvars and boolvars constructor
- Add Sat API (clauses)
- Fix `lex_chain_less` and `lex_chain_less_eq
- Add interface to parallel portfolio

# pychoco 0.1.2

Fix a few bugs and includes the `solver.limit_time(time_limit_string)` function. We also illustrated a few use cases in `docs/notebooks`. 

# pychoco 0.1.1

First release of pychoco, includes most features of Choco-solver. Extensively tested but still a beta release, we are open to feedbacks !