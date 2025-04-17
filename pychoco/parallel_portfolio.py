from pychoco import Model
from pychoco._handle_wrapper import _HandleWrapper
from pychoco.backend import create_parallel_portfolio, steal_nogoods_on_restarts, add_model, pf_solve, get_best_model, \
    get_best_solution
from pychoco.solution import Solution


class ParallelPortfolio(_HandleWrapper):
    """
    A Portfolio helper.
    The ParallelPortfolio resolution of a problem is made of four steps:

        1. adding models to be run in parallel,
        2. running resolution in parallel,
        3. getting the model which finds a solution (or the best one), if any.

    Each of the four steps is needed and the order is imposed too. In particular, in step 1. each model should be
    populated individually with a model of the problem (presumably the same model, but not required). Populating model
    is not managed by this class and should be done before applying step 2 with a dedicated method for instance. Note
    also that there should not be pending resolution process in any models. Otherwise, unexpected behaviors may occur.

    The resolution process is synchronized. As soon as one model ends (naturally or by hitting a limit) the other ones
    are eagerly stopped. Moreover, when dealing with an optimization problem, cut on the objective variable's value is
    propagated to all models on solution.

    It is essential to eagerly declare the objective variable(s) with {@link Model#setObjective(boolean, Variable)}.
    Note that the similarity of the models declared is not required. However, when dealing with an optimization
    problem, keep in mind that the cut on the objective variable's value is propagated among all models, so different
    objectives may lead to wrong results.

    Since there is no condition on the similarity of the models, once the resolution ends, the model which finds the
    (best) solution is internally stored.
    """

    def __init__(self, search_auto_conf: bool = True):
        """
        Constructor.
        :param search_auto_conf: Changes the search heuristics of the different solvers, except the first one
                                 (true by default). Must be set to false if search heuristics of the different threads
                                 are specified manually, so that they are not erased.
        """
        self.search_auto_conf = search_auto_conf
        handle = create_parallel_portfolio(search_auto_conf)
        super(ParallelPortfolio, self).__init__(handle)

    def steal_nogoods_on_restarts(self):
        """
        Calling this method will ensure that workers equipped with a restart policy not only record nogoods from
        themselves but also based on other workers of the portfolio.

        It is assumed that all models in this portfolio are equivalent (ie, each variable has the same ID in
        each worker).
        """
        steal_nogoods_on_restarts(self._handle)

    def add_model(self, model: Model, reliable: bool = True):
        """
        Adds a model to the list of models to run in parallel. The model can either be a fresh one, ready for
        populating, or a populated one.

        Important: the populating process is not managed by this parallel portfolio and should be done externally,
        with a dedicated method for example.

        When dealing with optimization problems, the objective variables <b>HAVE</b> to be declared eagerly with
        model.set_objective(variable, boolean).

        A reliable model is expected to prove the absence of a solution, improving one in the case of optimisation
        problem. A model with non-redundant constraints posted to improve resolution at the expense of completeness
        is considered unreliable. An unreliable model cannot share its no-goods and when it stops, cannot stop other
        models. There should be at least one reliable model in a portfolio. Otherwise, solving may be made incomplete.
        """
        add_model(self._handle, model._handle, reliable)

    def solve(self):
        """
        Run the solve() instruction of every model of the portfolio in parallel.
        Note that a call to get_best_model() returns a model which has found the best solution.
        :return True if and only if at least one new solution has been found.
        """
        return pf_solve(self._handle)

    def get_best_model(self):
        """
        Returns the first model from the list which, either :
            - finds a solution when dealing with a satisfaction problem,
            - or finds (and possibly proves) the best solution when dealing with an optimization problem.
        or None if no such model exists.
        Note that there can be more than one "finder" in the list, yet, this method returns the index of the first one.
        :return the first model which finds a solution (or the best one) or None if no such model exists.
        """
        handle = get_best_model(self._handle)
        return Model(_handle=handle)

    def find_best_solution(self):
        """
        Start solve and returns the best solution found.
        :return The best solution found.
        """
        handle = get_best_solution(self._handle)
        return Solution(handle)
