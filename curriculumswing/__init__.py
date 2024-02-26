__version__ = "1.4.0"

from .elective import Elective
from .swing import swing_calc
from .minmax import min_complexity, max_complexity, dummy_max, add_courses
from .catalog import make_catalog
__all__ = ["Elective", "swing_calc", "min_complexity", "max_complexity", "dummy_max", "add_courses", "make_catalog"]