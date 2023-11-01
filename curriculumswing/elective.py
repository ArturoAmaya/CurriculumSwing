from curricularanalytics import LearningOutcome, AbstractCourse, Course, CourseCollection, Requisite
from typing import List, Optional, Dict


# this is a mutated version of CourseCollection, just to not mutate the library until this concept works
# this is a general concept of an elective, a class that isn't "real", you just replace it with something else that is a real course
class Elective(AbstractCourse):
    courses: List[AbstractCourse]
    "All the equivalent courses"

    name: str
    credit_hours: float
    idx: str # this is the index in courses that the course will emulate
    active: bool # is it acting as an elective or as a real course? True is real course

    # these are the nominal 
    elective_requisites: Dict[int, Requisite]

    def __init__(
        self,
        elective_name: str,
        courses: List[AbstractCourse],
        idx: int,
        active: bool,
        *,
        learning_outcomes: Optional[List[LearningOutcome]] = None,
        institution: str = "",
        college: str = "",
        department: str = "",
        canonical_name: str = "",
        id: int = 0,
    ) -> None:
        "Constructor"
        self.name = elective_name
        self.credit_hours = courses[idx].credit_hours
        self.courses = courses
        self.active = active
        self.institution = institution
        if id == 0:
            self.id = self.default_id()
        else:
            self.id = courses[idx].id
        self.college = college
        self.department = department
        self.canonical_name = canonical_name
        self.requisites = {}
        # self.requisite_formula
        self.metrics = {
            "blocking factor": -1,
            "centrality": -1,
            "complexity": -1,
            "delay factor": -1,
            "requisite distance": -1,
        }
        self.metadata = {}
        self.learning_outcomes = learning_outcomes or []
        self.vertex_id = {}  # curriculum id -> vertex id

    def default_id(self) -> int:
        return hash(self.name + self.institution + str(len(self.courses)))

    def copy(self) -> "CourseCollection":
        return CourseCollection(
            self.name,
            [course.copy() for course in self.courses],
            self.idx,
            learning_outcomes=self.learning_outcomes,
            institution=self.institution,
            canonical_name=self.canonical_name,
        )
    
    # TODO
    def __repr__(self) -> str:
        return f"Course(idx={self.idx}, courses={self.courses}, name={repr(self.name)}, credit_hours={self.credit_hours}, institution={self.institution}, college={repr(self.college)}, department={repr(self.department)}, canonical_name={repr(self.canonical_name)}, requisites={self.requisites}, learning_outcomes={self.learning_outcomes}, metrics={self.metrics}, metadata={self.metadata})"

    # overriden methods

    # passthrough is for when you want to modify the original course, otherwise it's weird to edit a course through the elective
    def add_requisite(self, requisite_course: AbstractCourse, requisite_type: Requisite, passthrough: bool = False) -> None:
        # if it's passthrough and the elective is active
        if passthrough and self.active:
            return self.courses[self.idx].add_requisite(requisite_course, requisite_type)
        # else add a requisite to the elective itself
        else:
            self.requisites[requisite_course.id] = requisite_type

    
    # same as above
    def add_requisites(self, requisite_courses: List[AbstractCourse], requisite_types: List[Requisite], passthrough: bool = False) -> None:
        if passthrough and self.active:
            return self.courses[self.idx].add_requisites(requisite_courses, requisite_types)
        # else add to the elective itself
        else:
            assert len(requisite_courses) == len(requisite_types)
            for i in range(len(requisite_courses)):
                self.requisites[requisite_courses[i].id] = requisite_types[i]

    
    def delete_requisite(self, requisite_course: AbstractCourse, passthrough: bool = False) -> None:
        if passthrough and self.active:
            return self.courses[self.idx].delete_requisite(requisite_course)
        else:
            del self.requisites[requisite_course.id]

    # TODO the full match
    #def match(self, other: AbstractCourse, match_criteria: List[MatchCriterion] = ..., passthrough: bool = False) -> bool:
    #    if passthrough and self.active:
    #        return self.courses[self.idx].match(other, match_criteria)
        # else do nothing

    # TODO the full match
    #def find_match(self, course_set: List[AbstractCourse], match_criteria: List[MatchCriterion] = ..., passthrough:bool=False) -> AbstractCourse | None:
    #    if passthrough and self.active:
    #        return self.courses[self.idx].find_match(course_set, match_criteria)
        
    # special methods
    def update(self, new_idx:int=-1)->None:
        if new_idx <= -1:
            self.idx = self.idx
        else:
            # update!
            self.idx = new_idx
            self.requisites = self.courses[self.idx].requisites

    def set_passthrough(self, new_passthrough:bool)->None:
        self.passthrough = new_passthrough
    
    
    
