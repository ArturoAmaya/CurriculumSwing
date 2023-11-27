from curricularanalytics import Curriculum, Course
from curricularanalyticsdiff.HelperFns import course_from_name
from typing import Dict, List
import copy
from collections import OrderedDict

def add_course(curr: Curriculum, course_name:str, catalog:List[Course])->Curriculum:
    
    # find the course in question
    course = copy.deepcopy(next(c for c in catalog if c.name == course_name))
    new_curr = copy.deepcopy(curr)
    # for each of its prereqs
    for prereq_id in list(course.requisites):
        # check if that prereq exists in the curr
        ## to do that get the name
        if course.requisites[prereq_id] == "pre":
            prereq = next(c for c in catalog if c.id == prereq_id)
            if not (prereq.name in [c.name for c in new_curr.courses] or prereq.name in [c.prefix + ' ' + c.num for c in new_curr.courses]):
                # if it's not in there, add it
                new_curr = add_course(new_curr, prereq.name, catalog)
            # else nothing it's already there
            # actually there is stuff to be done if it is in there: make sure it's hooked up right: delete the existing one and replace with the one in the curriculum
            elif course_from_name(prereq.name, new_curr).id != prereq_id: #i.e. if the prereq names match but the ids don't bc one was read from file and has a lame low-number id
                del course.requisites[prereq_id]
                course.add_requisite(course_from_name(prereq.name, new_curr), "pre")
    return Curriculum(new_curr.name, new_curr.courses + [course], system_type=new_curr.system_type)


def add_impact(curr:Curriculum, courses: List[str], catalog:List[Course])->List[tuple[float, Course]]:
    # to calculate the impact just add the course
    ret = []
    for course_name in courses:
        # add course to curr
        new_curr = add_course(curr, course_name, catalog)
        # calculate metrics and subtract
        curr.basic_metrics()
        new_curr.basic_metrics()
        ret.append((new_curr.metrics['complexity'][0] - curr.metrics['complexity'][0], course_name))
    return ret

def min_complexity(curr: Curriculum, reqs: List[tuple[int, List[str]]], catalog: List[Course])->Curriculum:
    
    # step 1: calculate the add impact of each course in reqs
    ## first make a list from the set of all unique courses in reqs
    flat_reqs = []
    for elective in reqs:
        for course in elective[1]:
            flat_reqs.append(course)
    flat_reqs = sorted(list(set(flat_reqs)))

    impacts = add_impact(curr, flat_reqs, catalog)
    # step 1.5 organize the courses

    # step 2 choose the minimum courses that satisfy reqs

    # step 3 add the chosen courses in, calculate stats and return 
    pass
