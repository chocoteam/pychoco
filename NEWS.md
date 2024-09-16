# pychoco 0.2.0

- Update to choco-solver 4.10.16
- Add `bounded_domain` option in intvar
- Add reification constraints
- Add `pick_on_dom` and `pick_on_fil` search strategies
- Add `show_restarts` in solver

Todo:
- Add smart tables (or hybrid tables)
- Add partial assignment generator

# pychoco 0.1.2

Fix a few bugs and includes the `solver.limit_time(time_limit_string)` function. We also illustrated a few use cases in `docs/notebooks`. 

# pychoco 0.1.1

First release of pychoco, includes most features of Choco-solver. Extensively tested but still a beta release, we are open to feedbacks !