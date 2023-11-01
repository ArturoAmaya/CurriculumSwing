from curricularanalytics import Curriculum, Course
from typing import Dict, List
import copy
from collections import OrderedDict

# add a course from the 
def add_course_from_catalog(course_name: str, curr:Curriculum, catalog: List[Course]):
    # get the course
    course = next(c for c in catalog if c.name == course_name)
    new_curr = curr
    # get the prereqs and make sure they're all in there
    for prereq_id in course.requisites:
        if course.requisites[prereq_id] == "pre":
            prereq = next(c for c in catalog if c.id == prereq_id)
            if not prereq.name in [c.name for c in curr.courses]:
                # if it's not in there, add it
                new_curr = add_course_from_catalog(prereq.name, curr, catalog)
            # else nothing it's already there
    # add in this course
    t = copy.deepcopy(new_curr.courses)
    t.append(course)
    return Curriculum("new curr", t)
                   


# find the course in the curriculum, electives or catalog then add it and its prereqs
def add_course(curriculum: Curriculum, electives:OrderedDict, course: str, catalog: List[Course]):
    new_curr = None
    # find the course to extract its prereq info
    if course in [c.name for c in curriculum.courses]:
        # in this case, somethings up, let's leave that alone for now
        # TODO
        # in the brute form, do nothing
        new_curr = curriculum
    elif course in electives.keys():
        # in this case the chosen course is also an elective, put it in the curriculum and we'll work down 
        # electives have no prereqs, easy 
        new_curr = Curriculum(curriculum.name, copy.deepcopy(curriculum.courses).append(Course(course, 4.0)))
        pass
    elif course in [c.name for c in catalog]:
        # TODO
        # this is the hard one. presumably each key-val is the end of its own sequence, but in the case that it isn't we can modify curriculardiff using catalog
        new_curr = add_course_from_catalog(course, curriculum, catalog)
    return new_curr

def course_from_name(name:str, li:List[Course])->Course:
    for course in li:
        if course.name == name:
            return course

# remove course from curriculum
def remove_elective_curr(name:str, curr:Curriculum)->Curriculum:
    t = copy.deepcopy(curr.courses)
    t.remove(course_from_name(name, t))
    return Curriculum(curr.name, t)


# remove from the dict of electives
def remove_elective_dict(name: str, electives: OrderedDict, course: str)->OrderedDict:
    # easy remove the entry
    new_electives = copy.deepcopy(electives)
    del new_electives[name]

    # then remove course from new_electives lists
    for elective, course_list in new_electives.items():
        if course in course_list:
            course_list.remove(course)
    return new_electives

# take a OrderedDict (order matters)
# keys are elective names
# values are lists of course names
# ex. {
# TE 1: ["MAE 101", "MAE 102", "MAE 104"]}
def swing_calc(template: Curriculum, electives: OrderedDict[str, List[str]], catalog: List[Course]):
    my_results = [(0,0), (10000,0)]
    print("Loop!:", electives)
    if len(electives) == 0:
        return [(template.complexity()[0], template), (template.complexity()[0],template)]
    # for elective in electives
    for elective, courses in electives.items():
        # for course in electives
        for course in courses:
            # make a template copy, insert the chosen elective and remove the elective placeholder
            new_template = copy.deepcopy(template) # and then the other stuff

            # TODO: insert the chosen elective: 
            #   find the chosen elective (curriculum, electives or catalog, b/c the electives should be able to nest)
            new_curr = add_course(new_template, electives, course, catalog)

            # TODO: remove elective from curriculum
            new_curr = remove_elective_curr(elective, new_curr)
            # copy electives dict and remove elective (& every mention of course)
            new_electives = remove_elective_dict(elective, electives, course)
            # get results recursively
            results = swing_calc(new_curr, new_electives, catalog)

            if results[0][0] > my_results[0][0]:
                my_results[0] = results[0]
            if results[1][0] < my_results[1][0]:
                my_results[1] = results[1]
    return my_results


# # TODO better test case
# import curricularanalytics as ca
# # template = ca.read_csv("./files/SY-Curriculum Plan-CS26.csv")

# # create a lump of classes
# c1 = Course("MATH 20A", 4.0)
# c2 = Course("MATH 20B", 4.0)
# c2.add_requisite(c1, "pre")
# c3 = Course("MATH 18", 4.0)
# c4 = Course("MATH 20C", 4.0)
# c4.add_requisite(c2, "pre")
# c4.add_requisite(c3, "pre")
# c5 = Course("MATH 20D", 4.0)
# c5.add_requisite(c4, "pre")
# c6 = Course("MATH 20E", 4.0)
# c6.add_requisite(c5, "pre")

# c7 = Course("CSE 11", 4.0)
# c7.add_requisite(c1, "pre")

# c8 = Course("CSE 12", 4.0)
# c8.add_requisite(c7, "pre")

# c9 = Course("CSE 30", 4.0)
# c9.add_requisite(c8, "pre")

# c10 = Course("MAE 101", 4.0)
# c10.add_requisite(c4, "pre")
# c11 = Course("MAE 102", 4.0)
# c11.add_requisite(c10, "pre")
# c12 = Course("MAE 104", 4.0)
# c12.add_requisite(c6, "pre")

# c13 = Course("CSE 101", 4.0)
# c13.add_requisite(c5, "pre")
# c14 = Course("CSE 102", 4.0)
# c14.add_requisite(c13, "pre")
# c15 = Course("CSE 104", 4.0)
# c15.add_requisite(c8, "pre")

# c16 = Course("TE 1", 4.0)
# c17 = Course("TE 2", 4.0)
# catalog = [c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15, c16, c17]

# electives = dict()
# electives["TE 1"] = ["MAE 101", "MAE 102", "MAE 104"]
# electives["TE 2"] = ["CSE 101", "CSE 102", "CSE 104"]
# # skip math 20e
# template = Curriculum("C 1", [c1,c2,c3,c4,c5,c7,c8,c9, c16, c17])

# results = swing_calc(template, electives, catalog)
# print(results[0][0], results[1][0])

# print([course.name for course in results[0][1].courses])
# print([course.name for course in results[1][1].courses])