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