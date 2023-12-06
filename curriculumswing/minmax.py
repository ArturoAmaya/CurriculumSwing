from curricularanalytics import Curriculum, Course
from curricularanalyticsdiff.HelperFns import course_from_name
from typing import Dict, List
import copy
from collections import OrderedDict
import random

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


def add_impact(curr:Curriculum, courses: List[str], catalog:List[Course])->List[tuple[float, str]]:
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

def organize_impacts(impacts: List[tuple[float, str]], reqs: List[tuple[int, List[str]]], max: bool)->List[tuple[float, str, List[int]]]:
    # if max is true, organize in descending order else organize in ascending order
    
    # two options: go through impacts and find which req of reqs they're in
    # OR go through reqs and keep track of the courses they have. I will do option one - slightly slower but easier to read
    sorted_impacts = sorted(impacts, key=lambda tup: tup[0], reverse=max)
    organized_impacts = []
    for impact in sorted_impacts:
        ocurrences = [l_index for l_index in range(len(reqs)) if impact[1] in reqs[l_index][1]]
        organized_impacts.append((impact[0], impact[1], ocurrences))
    return organized_impacts

def remaining_origins(req_counts: List[int], electives_satisfied: List[int]):
    count = []
    for elective in electives_satisfied:
        if req_counts[elective] > 0:
            count.append(elective)
    return count

def choose_courses_min(organized_impacts: List[tuple[float, str, List[int]]], reqs: List[tuple[int, List[str]]]):
    req_counts = [req[0] for req in reqs] # flat list of ints. each one is the remaining number of courses ot choose for that list (corresponding by index so req_counts[i] is remaining # of courses for req[i])
    chosen_courses = [[] for req in reqs] # The final choices of courses chosen_courses[i] is a list of courses chosen to match reqs[i]
    for impact_tup in organized_impacts:
        impact, course_name, electives_satisfied = impact_tup
        empty_origins = [True if req_counts[idx] == 0 else False for idx in electives_satisfied]
        if all(count == 0 for count in req_counts):
                break
        if len(electives_satisfied) == 0 or all(empty_origins): # if the elective satisfies nothing (??) or all of its origins are empty, ignore it
            continue
        if len(electives_satisfied) == 1 and req_counts[electives_satisfied[0]] > 0: # if it has one open origin and that origin still has classes remaining
            chosen_courses[electives_satisfied[0]].append(course_name)
            req_counts[electives_satisfied[0]]-=1
        open_slots = remaining_origins(req_counts, electives_satisfied) # which indices are empty?
        if len(electives_satisfied) > 1 and len(open_slots) == 1:
            # add it into the to the list corresponding to 
            chosen_courses[open_slots[0]].append(course_name)
            req_counts[open_slots[0]]-=1
        if len(electives_satisfied) > 1 and len(open_slots)>1: # if has more than one non-full origin
            # look at those origins' remaining course_counts
            # for each such origin, look at the [remaining_course_count]-th course that satisfies that origin.
            # compare the impacts, choose the least bad one.
            look_ahead_impacts = []
            for open_slot in open_slots:
                look_ahead_count = req_counts[open_slot] # this is how many to look ahead to
                has_my_origin = list(filter(lambda x: open_slot in x[2], organized_impacts)) # which courses have the same open slot
                has_my_origin_future = has_my_origin[has_my_origin.index(impact_tup):] #courses down the list that ^^ (inlcude current for easier list indexing)
                down_the_line_choice = has_my_origin_future[look_ahead_count]
                look_ahead_impacts.append(down_the_line_choice[0]) # TODO check if we should use only the last value or the sum of all the values. I think it's just the last one
            
            # ok we have the impacts of each of the choices if that open slot isn't picked. find the least-bad and add that one
            # for each value take the sum of the values in the list without it
            compound_look_ahead_impacts = [sum(look_ahead_impacts) - x for x in look_ahead_impacts]
            sorted_clah = sorted(compound_look_ahead_impacts)
            if sorted_clah[0] == sorted_clah[1]: # i.e. there is a tie for least bad
                # call the function with all the decisions that you could take at this point, pick the best and go from there
                min_choices = [idx for idx, x in enumerate(compound_look_ahead_impacts) if x == min(compound_look_ahead_impacts)]
                results = []
                for min_choice in min_choices:
                    # cut the input to take all the decisions
                    results.append(choose_courses_min(organized_impacts[organized_impacts.index(impact_tup)+1:], req_counts)) # cut me out

            else:
                min_index = compound_look_ahead_impacts.index(min(compound_look_ahead_impacts))

            # open_slots and compound_look_ahead_impacts should use the same indices
            chosen_courses[open_slots[min_index]].append(course_name)
            req_counts[open_slots[min_index]]-=1


            continue
        
    print(chosen_courses)

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

    organized_impacts = organize_impacts(impacts, reqs, False)
    # step 2 choose the minimum courses that satisfy reqs

    chosen_courses = choose_courses_min(organized_impacts, reqs)
    # step 3 add the chosen courses in, calculate stats and return 
    pass
