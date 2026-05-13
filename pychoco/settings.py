from pychoco import backend
from pychoco._handle_wrapper import _HandleWrapper
from pychoco._utils import get_int_array

class Settings(_HandleWrapper):
    """
    Settings of a model. 
    This object can be used to set settings of the problem.
    """

    def __init__(self):
        handle = backend.init_settings()
        super(Settings, self).__init__(handle)

    @property
    def handle(self):
        return self._handle_        

    def set_lcg(self, lcg: bool):
        """
        Set the LCG setting.
        :param lcg: If True, enables LCG, otherwise disables it.
        """
        backend.set_lcg(self.handle, lcg)

    def set_warn_user(self, warn_user: bool):
        """
        Set the WarnUser setting.
        :param warn_user: If True, enables WarnUser, otherwise disables it.
        """
        backend.set_warn_user(self.handle, warn_user)

    def set_check_declared_constraints(self, check_declared_constraints: bool):
        """
        Set the CheckDeclaredConstraints setting.
        :param check_declared_constraints: If True, checks declared constraints, otherwise disables it.
        """
        backend.set_check_declared_constraints(self.handle, check_declared_constraints)

    def set_check_declared_views(self, check_declared_views: bool):
        """
        Set the CheckDeclaredViews setting.
        :param check_declared_views: If True, checks declared views, otherwise disables it.
        """
        backend.set_check_declared_views(self.handle, check_declared_views)

    def set_check_declared_monitors(self, check_declared_monitors: bool):
        """
        Set the CheckDeclaredMonitors setting.
        :param check_declared_monitors: If True, checks declared monitors, otherwise disables it.
        """
        backend.set_check_declared_monitors(self.handle, check_declared_monitors)

    def set_max_dom_size_for_enumerated(self, max_dom_size_for_enumerated: int):
        """
        Set the MaxDomSizeForEnumerated setting.
        :param max_dom_size_for_enumerated: The maximum domain size for enumerated variables.
        """
        backend.set_max_dom_size_for_enumerated(self.handle, max_dom_size_for_enumerated)

    def set_min_cardinality_for_sum_decomposition(self, min_cardinality_for_sum_decomposition: int):
        """
        Set the MinCardinalityForSumDecomposition setting.
        :param min_cardinality_for_sum_decomposition: The minimum cardinality for sum decomposition.
        """
        backend.set_min_cardinality_for_sum_decomposition(self.handle, min_cardinality_for_sum_decomposition)

    def set_enable_table_substitution(self, enable_table_substitution: bool):
        """
        Set the EnableTableSubstitution setting.
        :param enable_table_substitution: If True, enables table substitution, otherwise disables it.
        """
        backend.set_enable_table_substitution(self.handle, enable_table_substitution)


    def set_max_tuple_size_for_substitution(self, max_tuple_size_for_substitution: int):
        """
        Set the MaxTupleSizeForSubstitution setting.
        :param max_tuple_size_for_substitution: The maximum tuple size for substitution.
        """
        backend.set_max_tuple_size_for_substitution(self.handle, max_tuple_size_for_substitution)

    def set_max_size_in_mb_to_use_compact_table(self, max_size_in_mb_to_use_compact_table: int):
        """
        Set the MaxSizeInMBToUseCompactTable setting.
        :param max_size_in_mb_to_use_compact_table: The maximum size in MB to use compact table.
        """
        backend.set_max_size_in_mb_to_use_compact_table(self.handle, max_size_in_mb_to_use_compact_table)

    def set_enable_sat(self, enable_sat: bool):
        """
        Set the EnableSAT setting.
        :param enable_sat: If True, enables SAT, otherwise disables it.
        """
        backend.set_enable_sat(self.handle, enable_sat)

    def set_swap_on_passivate(self, swap_on_passivate: bool):
        """
        Set the SwapOnPassivate setting.
        :param swap_on_passivate: If True, enables swap on passivate, otherwise disables it.
        """
        backend.set_swap_on_passivate(self.handle, swap_on_passivate)

    def set_print_all_undeclared_constraints(self, print_all_undeclared_constraints: bool):
        """
        Set the PrintAllUndeclaredConstraints setting.
        :param print_all_undeclared_constraints: If True, prints all undeclared constraints, otherwise disables it.
        """
        backend.set_print_all_undeclared_constraints(self.handle, print_all_undeclared_constraints)

    def set_nb_max_learnt_clauses(self, nb_max_learnt_clauses: int):
        """
        Set the NbMaxLearntClauses setting.
        :param nb_max_learnt_clauses: The maximum number of learnt clauses.
        """
        backend.set_nb_max_learnt_clauses(self.handle, nb_max_learnt_clauses)