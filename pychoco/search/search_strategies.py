import time
from abc import ABC, abstractmethod


class SearchStrategies(ABC):
    """
    Abstract base class defining search strategies that can be applied to a solver.
    """

    @abstractmethod
    def set_default_search(self):
        """
        Set the solver's default search strategy.
        """
        pass

    @abstractmethod
    def set_dom_over_w_deg_search(self, *intvars):
        """
        Assignment strategy which selects a variable according to DomOverWDeg and assign
        it to its lower bound. This is based on "Boosting Systematic Search by Weighting Constraints."
        Boussemart et al. ECAI 2004.
        <a href="https://dblp.org/rec/conf/ecai/BoussemartHLS04">https://dblp.org/rec/conf/ecai/BoussemartHLS04</a>
        :param intvars: IntVars to use in the search strategy.
        """
        pass

    @abstractmethod
    def set_dom_over_w_deg_ref_search(self, *intvars):
        """
        Assignment strategy which selects a variable according to <code>refined DomOverWDeg</code> and assign
        it to its lower bound, where the weight incrementer is "ca.cd".
        This is based on "Refining Constraint Weighting." Wattez et al. ICTAI 2019.
        <a href="https://dblp.org/rec/conf/ictai/WattezLPT19">https://dblp.org/rec/conf/ictai/WattezLPT19</a>
        :param intvars: IntVars to use in the search strategy.
        """
        pass

    @abstractmethod
    def set_activity_based_search(self, *intvars):
        """
        Create an Activity based search strategy.
        Uses public static parameters
        (GAMMA=0.999d, DELTA=0.2d, ALPHA=8, RESTART=1.1d, FORCE_SAMPLING=1)
        This is based on "Activity-Based Search for Black-Box Constraint Programming Solvers."
        Michel et al. CPAIOR 2012.
        <a href="https://dblp.org/rec/conf/cpaior/MichelH12">https://dblp.org/rec/conf/cpaior/MichelH12</a>
        :param intvars: IntVars to use in the search strategy.
        """
        pass

    @abstractmethod
    def set_min_dom_lb_search(self, *intvars):
        """
        Assigns the non-instantiated variable of the smallest domain size to its lower bound.
        :param intvars: IntVars to use in the search strategy.
        """
        pass

    @abstractmethod
    def set_min_dom_ub_search(self, *intvars):
        """
        Assigns the non-instantiated variable of smallest domain size to its upper bound.
        :param intvars: IntVars to use in the search strategy.
        """
        pass

    @abstractmethod
    def set_random_search(self, seed: int = round(time.time()), *intvars):
        """
        Randomly selects a variable and assigns it to a value randomly taken in - the domain in case
        the variable has an enumerated domain - {LB,UB} (one of the two bounds) in case the domain is
        bounded
        :param seed: seed for random
        :param intvars: IntVars to use in the search strategy.
        """
        pass

    @abstractmethod
    def set_conflict_history_search(self, *intvars):
        """
        Assignment strategy which selects a variable according to <code>Conflict History</code>
        and assigns it to its lower bound.
        This is based on "Conflict history based search for constraint satisfaction problem."
        Habet et al. SAC 2019.
        <a href="https://dblp.org/rec/conf/sac/HabetT19">https://dblp.org/rec/conf/sac/HabetT19</a>
        :param intvars: IntVars to use in the search strategy.
        """
        pass

    @abstractmethod
    def set_input_order_lb_search(self, *intvars):
        """
        Assigns the first non-instantiated variable to its lower bound.
        :param intvars: IntVars to use in the search strategy.
        """
        pass

    @abstractmethod
    def set_input_order_ub_search(self, *intvars):
        """
        Assigns the first non-instantiated variable to its upper bound.
        :param intvars: IntVars to use in the search strategy.
        """
        pass

    @abstractmethod
    def set_failure_length_based_search(self, *intvars):
        """
        Assignment strategy which selects a variable according to <code>Failure length based</code>
        variable ordering and assigns it to its lower bound.
        This is based on "Failure Based Variable Ordering Heuristics for Solving CSPs."
        H. Li, M. Yin, and Z. Li, CP 2021.
        <a href="https://dblp.org/rec/conf/cp/LiYL21">https://dblp.org/rec/conf/cp/LiYL21</a>
        :param intvars: IntVars to use in the search strategy.
        """
        pass

    @abstractmethod
    def set_failure_rate_based_search(self, *intvars):
        """
        Assignment strategy which selects a variable according to <code>Failure rate based</code>
        variable ordering and assigns it to its lower bound.
        This is based on "Failure Based Variable Ordering Heuristics for Solving CSPs."
        H. Li, M. Yin, and Z. Li, CP 2021.
        <a href="https://dblp.org/rec/conf/cp/LiYL21">https://dblp.org/rec/conf/cp/LiYL21</a>
        :param intvars: IntVars to use in the search strategy.
        """
        pass
