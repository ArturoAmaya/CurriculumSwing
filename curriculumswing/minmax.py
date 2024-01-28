from curricularanalytics import Curriculum, Course
from curricularanalyticsdiff.HelperFns import course_from_name
from typing import Dict, List
import copy
from collections import OrderedDict
import random
from itertools import combinations

def add_course_prereqs_to_choice(course: Course, catalog: List[Course], reqs: List[tuple[int, List[str]]], req_counts: List[int], chosen_courses: List[List[str]], organized_impacts, curr:Curriculum):
    # loop through the prerequisites
    prerequisites = [catalog[[c.id for c in catalog].index(p)] for p in course.requisites]
    curr_course_list = [c.name for c in curr.courses]
    prerequisites = list(filter(lambda x: x.name not in curr_course_list, prerequisites))

    req_counts_t = copy.deepcopy(req_counts)
    chosen_courses_t = copy.deepcopy(chosen_courses)
    for preq in prerequisites:
        # add in the prereqs, recursively

        # find the impact tuple with its allowed slots
        try: 
            tup = [t for t in organized_impacts if t[1] == preq.name][0] # list comp is easy but there should only be one such tuple
        except: 
            tup = (0, course.name, [])
        # select the first open slot and put it in there
        open_slot = None
        try:
            open_slot = next(i for i,v in enumerate(req_counts_t) if (v > 0 and i in tup[2]))
            chosen_courses_t[open_slot].append(preq.name)
            req_counts_t[open_slot] -= 1
        except:
            pass # in this case, we're tanking the prereq - it satisfies nothing by itself but we need it for the course we're adding
        # recurse down its prereqs
        if preq.requisites:
            (chosen_courses_t, req_counts_t)= add_course_prereqs_to_choice(preq, catalog, reqs, req_counts_t, chosen_courses_t, organized_impacts, curr)
    return chosen_courses_t, req_counts_t

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

def add_courses(curr:Curriculum, courses:List[List[str]], catalog:List[Course])->Curriculum:
    new_curr = copy.deepcopy(curr)
    for elective_list in courses:
        for course in elective_list:
            if course not in [c.name for c in new_curr.courses]: # only add in if it's not there already
                new_curr = add_course(new_curr, course, catalog)
    return new_curr

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

def merge_results(recursion_results: tuple[List[List[str]], float], current_chosen_courses: List[List[str]], req_counts: List[int]):
    # simply make a blank list of lists and add the contents of recursion 
    # results in and then the results of current chosen courses. then count 
    # how many in each list and adjust req_counts accordingly
    merged_results = copy.deepcopy(current_chosen_courses)
    for idx, elective_list in enumerate(merged_results):
        for elective in recursion_results[0][idx]:
            elective_list.append(elective)
            req_counts[idx]-=1
    return (merged_results, req_counts)


def choose_courses_min(organized_impacts: List[tuple[float, str, List[int]]], reqs: List[tuple[int, List[str]]]):
    req_counts = [req[0] for req in reqs] # flat list of ints. each one is the remaining number of courses ot choose for that list (corresponding by index so req_counts[i] is remaining # of courses for req[i])
    chosen_courses = [[] for req in reqs] # The final choices of courses chosen_courses[i] is a list of courses chosen to match reqs[i]
    total_impact = 0
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
            total_impact += impact

        open_slots = remaining_origins(req_counts, electives_satisfied) # which indices are empty?
        if len(electives_satisfied) > 1 and len(open_slots) == 1:
            # add it into the to the list corresponding to 
            chosen_courses[open_slots[0]].append(course_name)
            req_counts[open_slots[0]]-=1
            total_impact += impact

        if len(electives_satisfied) > 1 and len(open_slots)>1: # if has more than one non-full origin
            # look at those origins' remaining course_counts
            # for each such origin, look at the [remaining_course_count]-th course that satisfies that origin.
            # compare the impacts, choose the least bad one.
            look_ahead_impacts = []
            not_done = True
            for open_slot in open_slots:
                look_ahead_count = req_counts[open_slot] # this is how many to look ahead to
                has_my_origin = list(filter(lambda x: open_slot in x[2], organized_impacts)) # which courses have the same open slot
                has_my_origin_future = has_my_origin[has_my_origin.index(impact_tup):] #courses down the list that ^^ (inlcude current for easier list indexing)
                if len(has_my_origin_future) == 0: 
                    # there's no other ones that satisfy that choice so pick that one
                    chosen_courses[open_slot].append(course_name)
                    req_counts[open_slot]-=1
                    total_impact += impact
                    not_done == False
                    break
                down_the_line_choice = has_my_origin_future[look_ahead_count]
                look_ahead_impacts.append(down_the_line_choice[0]) # TODO check if we should use only the last value or the sum of all the values. I think it's just the last one
            if (not_done):
                # ok we have the impacts of each of the choices if that open slot isn't picked. find the least-bad and add that one
                # for each value take the sum of the values in the list without it
                compound_look_ahead_impacts = [sum(look_ahead_impacts) - x for x in look_ahead_impacts]
                sorted_clah = sorted(compound_look_ahead_impacts)
                # in early tests, the tiebreaking leads to a ton of recursion that seems to behave exactly like trying all the options.
                # let's use a heuristic along the lines of if the next x courses all have the same exact impact don't recurse and just pick the first one
                # for now let's say the lookahead value is 3 * the total number for remaining reqs. 3 should really depend on the density of the choices, but whatever TODO
                heuristic_lookahead = 3 * sum(req_counts)
                #round(organized_impacts[organized_impacts.index(impact_tup) + heuristic_lookahead][0], 1) == round(impact,1):
                if sorted_clah[0] == sorted_clah[1] and round(organized_impacts[organized_impacts.index(impact_tup) + heuristic_lookahead][0], 1) != round(impact,1): # i.e. there is a tie for least bad
                    # call the function with all the decisions that you could take at this point, pick the best and go from there
                    min_choices = [open_slots[idx] for idx, x in enumerate(compound_look_ahead_impacts) if x == min(compound_look_ahead_impacts)]
                    results = []
                    for min_choice in min_choices:
                        # cut the input to take all the decisions
                        results.append(choose_courses_min(organized_impacts[organized_impacts.index(impact_tup)+1:], [(req_counts[idx] - 1,elecs) if idx == min_choice else (req_counts[idx],elecs) for idx,(count, elecs) in enumerate(reqs)])) # cut me out
                        
                        
                    # find the index of the minimum impact
                    # from the smallest result find the min_choice that produced it
                    min_index = min_choices[results.index(min(results, key=lambda x: x[1]))]
                    # min choices and results share indices
                    chosen_courses[min_index].append(course_name)
                    req_counts[min_index] -= 1
                    total_impact += impact

                    (chosen_courses, req_counts) = merge_results(results[min_choices.index(min_index)], chosen_courses, req_counts)
                    # note that you've already traversed the tree you're about to traverse here.
                    # If you can merge the ongoing results with the minimum ones you just found you can 
                    # easily finish here.
                    total_impact += results[min_choices.index(min_index)][1]
                    return (chosen_courses, total_impact)
                else:
                    # if there's a clear winner find the index of the winner in the original list
                    min_index = compound_look_ahead_impacts.index(min(compound_look_ahead_impacts))
                    # open_slots and compound_look_ahead_impacts should use the same indices
                    chosen_courses[open_slots[min_index]].append(course_name)
                    req_counts[open_slots[min_index]]-=1
                    total_impact += impact
    return (chosen_courses, total_impact)

def choose_courses_max(organized_impacts: List[tuple[float,str,List[int]]],reqs: List[tuple[int, List[str]]], catalog: List[Course], curriculum: Curriculum):
    req_counts = [req[0] for req in reqs] # flat list of ints - each is the remaining number of courses to choose for that list (corresponding by index, so req_counts[i] is the remaining # of courses for req[i])
    chosen_courses = [[] for req in reqs] # the final choices of courses. chosen_courses[i] is a list of courses chosen to match reqs[i]
    total_impact = 0
    for impact_tup in organized_impacts:
        impact, course_name, electives_satisfied = impact_tup
        empty_origins = [True if req_counts[idx] == 0 else False for idx in electives_satisfied]
        if all(count == 0 for count in req_counts): # if we've satisfied all the requirements
            break
        if len(electives_satisfied) == 0 or all(empty_origins): # if the elective satisfied nothing or all of its origins are empty ignore it
            continue
        if len(electives_satisfied) == 1 and req_counts[electives_satisfied[0]] > 0: # if it has one open origin and that origin still has classes remaining
            chosen_courses[electives_satisfied[0]].append(course_name)
            req_counts[electives_satisfied[0]] -= 1
            total_impact += impact
            
            # for any choice, add in the prereqs too
            catalog_course = catalog[[c.name for c in catalog].index(course_name)]
            (chosen_courses, req_counts) = add_course_prereqs_to_choice(catalog_course, catalog, reqs, req_counts, chosen_courses, organized_impacts, curriculum)
        open_slots = remaining_origins(req_counts, electives_satisfied) # which indices are empty
        if len(electives_satisfied) > 1 and len(open_slots) == 1:
            # add it into the list corresponding to the only open slot
            chosen_courses[open_slots[0]].append(course_name)
            req_counts[open_slots[0]]-=1
            total_impact += impact
            # for any choice, add in the prereqs too
            catalog_course = catalog[[c.name for c in catalog].index(course_name)]
            (chosen_courses, req_counts) = add_course_prereqs_to_choice(catalog_course, catalog, reqs, req_counts, chosen_courses, organized_impacts, curriculum)
        if len(electives_satisfied) > 1 and len(open_slots) > 1: # if it has more than one non-full origin
            # look at those origins' reminaing course counts
            # for each such origin look at the [remaining_course_count]-th course that satisfies that origin.
            # compare the impacts, choose the worst one.
            look_ahead_impacts = []
            for open_slot in open_slots:
                look_ahead_count = req_counts[open_slot] # how many to look ahead by
                has_my_origin = list(filter(lambda x: open_slot in x[2], organized_impacts)) # which courses have the same open slot
                has_my_origin_future = has_my_origin[has_my_origin.index(impact_tup):] # courses down the list that ^^ (incldue current for easier list indexing)
                down_the_line_choice = has_my_origin_future[look_ahead_count]
                look_ahead_impacts.append(down_the_line_choice[0])

            # by now we have the impact of each of the choices if that open slot isn't picked find the worst one and add that one
            # for each value take the sum of the values in the list without it (i.e. the impact of picking that particular origin for the current course)
            compound_look_ahead_impacts = [sum(look_ahead_impacts)-x for x in look_ahead_impacts]
            sorted_clah = sorted(compound_look_ahead_impacts, reverse=True) # sort in descending order

            # in early minimizer tests previous tiebreaking methods lead to too much recursion that behaves on the order of trying every possible combination
            # currently using a heuristic that equates to: if the next x courses all have the same exact impact don't recurse and just pick the first one
            # for now let's say that lookahead value x is 2*the total number of remaining requirements. 3 shoudl depend on the density of the choices, but we can edit later
            heuristic_lookahead = 2*sum(req_counts)
            flag = True # for testing reasons
            if flag and sorted_clah[0] == sorted_clah[1] and round(organized_impacts[organized_impacts.index(impact_tup) + heuristic_lookahead][0], 1) != round(impact, 1): #i.e. there is a tie for most bad
                # call the function with all the decisions that you could take at this point, pick the worst and go from there
                max_choices = [open_slots[idx] for idx,x in enumerate(compound_look_ahead_impacts) if x == max(compound_look_ahead_impacts)]
                results = []
                choices = []
                for max_choice in max_choices:
                    # cut the input to take all the decisions already made into account

                    # to do add in the prereqs of this implied choice
                    # for any choice, add in the prereqs too
                    catalog_course = catalog[[c.name for c in catalog].index(course_name)]
                    reqs_temp = [(req_counts[idx] -1, elecs) if idx == max_choice else (req_counts[idx], elecs) for idx, (count,elecs) in enumerate(reqs)]
                    (chosen_courses_temp, req_counts_temp) = add_course_prereqs_to_choice(catalog_course, catalog, reqs_temp, [x[0] for x in reqs_temp], chosen_courses, organized_impacts, curriculum)
                    choices.append((chosen_courses_temp, req_counts_temp))
                    results.append(choose_courses_max(organized_impacts[organized_impacts.index(impact_tup)+1:], [(req_counts_temp[idx], elecs) for idx, (count,elecs) in enumerate(reqs)], catalog, curriculum)) # cut current one out
                
                # find the index of the max impact
                # from the the largest result find the max_choice that produced it
                max_index = max_choices[results.index(max(results, key=lambda x: x[1]))]
                # max choices and results share indices
                choices[max_choices.index(max_index)][0][max_index].append(course_name) # chosen_courses[max_index].append(course_name)
                #choices[max_choices.index(max_index)][1][max_index] -=1 #req_counts[max_index] -= 1

                total_impact += impact

                (chosen_courses, req_counts) = merge_results(results[max_choices.index(max_index)], choices[max_choices.index(max_index)][0], choices[max_choices.index(max_index)][1])

                total_impact += results[max_choices.index(max_index)][1]

                # TODO add in the prerequisites!
                return (chosen_courses, total_impact)
            else:
                # if there's a clear winner find the index of the winner in the original list
                max_index = compound_look_ahead_impacts.index(max(compound_look_ahead_impacts))
                # open_slots and compound lookahead impacts should use the same indices
                chosen_courses[open_slots[max_index]].append(course_name)
                req_counts[open_slots[max_index]] -= 1
                total_impact += impact
        # TODO: add in the prerequisites
        
    return (chosen_courses, total_impact)
 
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
    (chosen_courses, estimated_total_impact) = choose_courses_min(organized_impacts, reqs)

    # step 3 add the chosen courses in
    new_curr = add_courses(curr, chosen_courses, catalog)

    # step 4 calculate stats
    new_metrics = new_curr.complexity()[0]
    base_metrics = curr.complexity()[0]

    if ( round(new_metrics - base_metrics, 2) < round(estimated_total_impact, 2)):
        print("impact estimation error - estimated is ", round(estimated_total_impact, 2) / round(new_metrics - base_metrics, 2), " times actual")

    return (chosen_courses, new_curr)

def max_complexity(curr: Curriculum, reqs: List[tuple[int, List[str]]], catalog: List[Course]) -> Curriculum:
    # step 1 calculate the add impact of each course
    # but first make a list from the set of all unique courses in the reqs
    flat_reqs = []
    for elective in reqs:
        for course in elective[1]:
            flat_reqs.append(course)
    flat_reqs = sorted(list(set(flat_reqs)))

    impacts = add_impact(curr, flat_reqs, catalog)

    # organize the courses by impact
    organized_impacts = organize_impacts(impacts, reqs, True)

    # step 2 choose the max courses that satisfy reqs
    (chosen_courses, estimated_total_impact) = choose_courses_max(organized_impacts, reqs, catalog, curr)
    
    # step 3 add the chosen courses in
    new_curr = add_courses(curr, chosen_courses, catalog)

    # step 4 calculate stats
    new_complexity = new_curr.complexity()[0]
    base_complexity = curr.complexity()[0]

    if ( round(new_complexity - base_complexity, 2) > round(estimated_total_impact, 2)):
        print("impact estimation error - estimated is ", round(estimated_total_impact, 2) / round(new_metrics - base_metrics, 2), " times actual")

    return (chosen_courses, new_curr)

def double_courses(curr):
    ret = False
    names = [c.name for c in curr.courses]
    if len(set(names)) != len(names):
        return True
    else:
        return False

# DUMMY max choice
def dummy_max(curr:Curriculum, reqs: List[tuple[int, List[str]]], catalog: List[Course])->Curriculum:
    # for each req, pick classes, remove them from the other lists
    worst_impact = 0
    worst_curr = curr
    new_curr = curr
    for req in reqs:
        s = list(combinations(req[1], req[0]))
        for choice in s:
            for course in choice:
                new_curr = add_course(curr, course, catalog)
            (new_curr, impact) = dummy_max(new_curr, reqs[1:], catalog)
            if impact > worst_impact and not double_courses(new_curr):
                worst_impact = impact
                worst_curr = new_curr
    return (worst_curr, worst_curr.complexity()[0])

