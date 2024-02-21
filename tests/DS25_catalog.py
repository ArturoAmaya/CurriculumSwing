import sys
sys.path.append('./')
import curriculumswing as cs
import curricularanalytics as ca
from curricularanalytics import Course, quarter
from typing import List, OrderedDict
import random

########################################################
# CATALOG section
# Generate the catalog
catalog = []
def course_find(name:str, li:List[Course])->Course:
    for course in li:
        if course.name == name:
            return course

def add_course(name:str, units:float, catalog:List[Course], prereq_names:List[str]):
    c = Course(name, units)
    for preq in prereq_names:
        c.add_requisite(course_find(preq, catalog), "pre")
    catalog.append(c)
    return catalog

c1 = Course("MATH 20A", 4.0)
catalog.append(c1)
c2 = Course("MATH 20B", 4.0)
c2.add_requisite(c1, "pre")
catalog.append(c2)
c3 = Course("MATH 18", 4.0)
catalog.append(c3)
c4 = Course("MATH 20C", 4.0)
c4.add_requisite(c2, "pre")
catalog.append(c4)
c5 = Course("MATH 20D", 4.0)
c5.add_requisite(c4, "pre")
catalog.append(c5)

c6 = Course("MATH 20E", 4.0)
c6.add_requisite(c5, "pre")
c6.add_requisite(c3, "pre")
catalog.append(c6)

# lower div CSE
catalog = add_course("CSE 11", 4.0, catalog, [])
catalog = add_course("CSE 12", 4.0, catalog, ["CSE 11"])
catalog = add_course("CSE 15L", 4.0, catalog, ["CSE 11"])
catalog = add_course("CSE 20", 4.0, catalog, ["CSE 11"])
catalog = add_course("CSE 21", 4.0, catalog, ["CSE 20"])
catalog = add_course("CSE 30", 4.0, catalog, ["CSE 12", "CSE 15L"])


# lower div COGS
catalog = add_course("COGS 9", 4.0, catalog, [])
catalog = add_course("COGS 10", 4.0, catalog, [])
catalog = add_course("COGS 14A", 4.0, catalog, [])
catalog = add_course("COGS 14B", 4.0, catalog, [])
catalog = add_course("COGS 17", 4.0, catalog, [])
catalog =  add_course("COGS 18", 4.0, catalog, [])

# lower div BILD
catalog = add_course("BILD 1", 4.0, catalog, [])
catalog = add_course("BILD 3", 4.0, catalog, [])

# lower div social sciences TODO soci 60, usp 4
catalog = add_course("POLI 5", 4.0, catalog, [])
catalog = add_course("POLI 30", 4.0, catalog, [])

# soci lower div
catalog = add_course("SOCI 60", 4.0, catalog, [])

# USP lower div
catalog = add_course("USP 4", 4.0, catalog, [])

# lower div ECON
catalog = add_course("ECON 1", 4.0, catalog, [])
catalog = add_course("ECON 3", 4.0, catalog, ["ECON 1"])
catalog = add_course("ECON 5", 4.0, catalog, [])

# lower div comm
catalog = add_course("COMM 10", 4.0, catalog, [])

# lower div DSC
catalog = add_course("DSC 10", 4.0, catalog, [])
catalog = add_course("DSC 20", 4.0, catalog, ["DSC 10"])
catalog = add_course("DSC 30", 4.0, catalog, ["DSC 20"])
catalog = add_course("DSC 40A", 4.0, catalog, ["DSC 10", "MATH 20C", "MATH 18"])
catalog = add_course("DSC 40B", 4.0, catalog, ["DSC 20", "DSC 40A"])
catalog = add_course("DSC 80", 4.0, catalog, ["DSC 30", "DSC 40A"])
catalog = add_course("DSC 90", 2.0, catalog, ["DSC 10"])
catalog = add_course("DSC 95", 2.0, catalog, ["DSC 10"])
catalog = add_course("DSC 96", 2.0, catalog, [])
catalog = add_course("DSC 97", 4.0, catalog, ["MATH 20C", "MATH 18", "DSC 20", "DSC 40A"])
catalog = add_course("DSC 98", 4.0, catalog, ["MATH 20C", "MATH 18", "DSC 20", "DSC 40A"])
catalog = add_course("DSC 99", 4.0, catalog, ["MATH 20C", "MATH 18", "DSC 20", "DSC 40A"])

############################################################## UPPER DIV

# upper div MATH
catalog = add_course("MATH 109", 4.0, catalog, ["MATH 18", "MATH 20C"])
catalog = add_course("MATH 180A", 4.0, catalog, ["MATH 20C"])
catalog = add_course("MATH 189", 4.0, catalog, ["MATH 18", "MATH 20C", "MATH 180A"])
catalog = add_course("MATH 181A", 4.0, catalog, ["MATH 180A", "MATH 18", "MATH 20C"])
catalog = add_course("MATH 183", 4.0, catalog, ["MATH 20C"])
catalog = add_course("MATH 189", 4.0, catalog, ["MATH 18", "MATH 20C"]) # TODO fix this

# upper div CSE
catalog = add_course("CSE 100", 4.0, catalog, ["CSE 21", "CSE 12", "CSE 15L", "CSE 30"])
catalog = add_course("CSE 150A", 4.0, catalog, ["CSE 12" ]) # TODO fix this
catalog = add_course("CSE 151A", 4.0, catalog, ["CSE 12"]) # TODO fix this
catalog = add_course("CSE 158", 4.0, catalog, ["CSE 12"]) # TODO fix this

## upper div DSC
catalog = add_course("DSC 100", 4.0, catalog, ["DSC 40B", "DSC 80"])
catalog = add_course("DSC 102", 4.0, catalog, ["DSC 100"])
catalog = add_course("DSC 104", 4.0, catalog, ["DSC 100"])
catalog = add_course("DSC 106", 4.0, catalog, ["DSC 80"])
catalog = add_course("DSC 120", 4.0, catalog, ["MATH 18", "MATH 20C", "DSC 40B"])
catalog = add_course("DSC 140A", 4.0, catalog, ["DSC 80"])#, "ECE 109"]) TODO fix this
catalog = add_course("DSC 140B", 4.0, catalog, ["DSC 80"]) # TODO fix this
catalog = add_course("DSC 148", 4.0, catalog, ["DSC 40B", "DSC 80" ]) #TODO fix this
catalog = add_course("DSC 155", 4.0, catalog, ["MATH 180A", "MATH 18"])
catalog = add_course("DSC 160", 4.0, catalog, ["DSC 80"])
catalog = add_course("DSC 161", 4.0, catalog, ["ECON 5"]) # TODO fix this
catalog = add_course("DSC 167", 4.0, catalog, ["DSC 80"])
catalog = add_course("DSC 170", 4, catalog, ["DSC 80"])
catalog = add_course("DSC 180A", 4.0, catalog, ["DSC 102", "MATH 189", "DSC 148", "DSC 106"])
catalog = add_course("DSC 180B", 4.0, catalog, ["DSC 180A"])
catalog = add_course("DSC 190", 4.0, catalog, [])
catalog = add_course("DSC 191", 2.0, catalog, [])
#catalog = add_course("DSC 197", 4.0, catalog, [])
#catalog = add_course("DSC 198", 4.0, catalog, [])
#catalog = add_course("DSC 199", 4.0, catalog, [])


# ECON upper div
catalog = add_course("ECON 120A", 4.0, catalog, ["ECON 1", "MATH 20C"])

# Science Domain
# TODO PSYC 106
catalog = add_course("BICD 100", 4.0, catalog, ["BILD 1", "BILD 3"])
catalog = add_course("BIEB 174", 4.0, catalog, ["BILD 3"])
catalog = add_course("SIO 132", 4.0, catalog, ["BILD 3"])
catalog = add_course("SIO 109", 4.0, catalog, [])
catalog = add_course("POLI 117", 4.0, catalog, [])
catalog = add_course("ESYS 103", 4.0, catalog, ["MATH 20B"])

# from ml track
catalog = add_course("COGS 108", 4.0, catalog, ["DSC 10"])
# MAE 124 DNE
catalog = add_course("COGS 180", 4.0, catalog, ["COGS 17", "COGS 108", "MATH 18"]) # TODO fix
catalog = add_course("CSE 180", 4.0, catalog, ["BILD 1", "CSE 11"])
catalog = add_course("PSYC 106", 4.0, catalog, [])


# Social Sciences Track
catalog = add_course("COMM 106I", 4.0, catalog, ["COMM 10"])
catalog = add_course("PHIL 174", 4.0, catalog, [])
catalog = add_course("POLI 170A", 4.0, catalog, ["POLI 30"])
catalog = add_course("POLI 171", 4.0, catalog, ["POLI 5", "POLI 30"])
catalog = add_course("POLI 172", 4.0, catalog, ["POLI 5", "POLI 30"])
catalog = add_course("POLI 173", 4.0, catalog, [])
catalog = add_course("SOCI 102", 4.0, catalog, ["SOCI 60"])
catalog = add_course("SOCI 103M", 4.0, catalog, ["SOCI 60"])
catalog = add_course("SOCI 108", 4.0, catalog, ["SOCI 60"])
catalog = add_course("SOCI 109", 4.0, catalog, ["SOCI 60"])
catalog = add_course("SOCI 109M", 4.0, catalog, [])
catalog = add_course("SOCI 136", 4.0, catalog, [])
catalog = add_course("SOCI 165", 4.0, catalog, [])
catalog = add_course("SOCI 171", 4.0, catalog, [])
catalog = add_course("USP 122", 4.0, catalog, [])
catalog = add_course("USP 125", 4.0, catalog, [])
catalog = add_course("USP 138", 4.0, catalog, [])
catalog = add_course("USP 153", 4.0, catalog, [])
catalog = add_course("USP 172", 4.0, catalog, [])
catalog = add_course("USP 175", 4.0, catalog, [])
catalog = add_course("USP 180", 4.0, catalog, [])

# BUSINESS TRACK ELECTIVES
catalog = add_course("ECON 120B", 4.0, catalog, ["ECON 120A"]) # TODO fix this
catalog = add_course("ECON 120C", 4.0, catalog, ["ECON 120B"])
catalog = add_course("MATH 152", 4.0, catalog, ["MATH 20D", "MATH 18"])
catalog = add_course("MATH 173A", 4.0, catalog, ["MATH 20C", "MATH 18"])
catalog = add_course("MATH 173B", 4.0, catalog, ["MATH 173A"])
# math 180A
catalog = add_course("MATH 180B", 4.0, catalog, ["MATH 20D", "MATH 18", "MATH 109", "MATH 180A"])
catalog = add_course("MATH 180C", 4.0, catalog, ["MATH 180B"])
catalog = add_course("MATH 181A", 4.0, catalog, ["MATH 180A", "MATH 18", "MATH 20C"])
catalog = add_course("MATH 181B", 4.0, catalog, ["MATH 181A"])
catalog = add_course("MATH 181C", 4.0, catalog, ["MATH 181B"])
catalog = add_course("MATH 181D", 4.0, catalog, ["ECON 120A"]) # TODO fix this
catalog = add_course("MATH 181E", 4.0, catalog, ["MATH 181B"])
catalog = add_course("MATH 181F", 4.0, catalog, ["ECON 120A"]) # TODO fix this
catalog = add_course("MATH 194", 4.0, catalog, ["MATH 20D", "MATH 18", "MATH 180A"])
catalog = add_course("MGT 103", 4.0, catalog, [])
catalog = add_course("MGT 153", 4.0, catalog, ["MATH 18", "COGS 14B"]) # TODO fix this


catalog = add_course("COGS 118A", 4.0, catalog, ["COGS 18", "MATH 18", "MATH 20E", "COGS 108"])
# MACHINE LEARNING
# cogs 108 here too
catalog = add_course("COGS 109", 4.0, catalog, ["COGS 14B", "MATH 18", "CSE 11"])
catalog = add_course("COGS 118C", 4.0, catalog, ["MATH 18", "COGS 14B", "COGS 108"])
catalog = add_course("COGS 118D", 4.0, catalog, ["MATH 18", "MATH 180A", "COGS 108"])
catalog = add_course("COGS 120", 4.0, catalog, ["DSC 30", "COGS 10"]) # TODO fix this
catalog = add_course("CSE 170", 4.0, catalog, ["DSC 30", "COGS 10"])
catalog = add_course("COGS 121", 4.0, catalog, ["COGS 120", "DSC 30"]) # TODO fix this
catalog = add_course("COGS 181", 4.0, catalog, ["COGS 18", "MATH 18", "MATH 20E", "MATH 180A", "COGS 118A"]) # TODO fix this
catalog = add_course("CSE 151B", 4.0, catalog, ["MATH 20C", "ECON 120A"])
catalog = add_course("COGS 189", 4.0, catalog, ["COGS 108"])
catalog = add_course("CSE 106", 4.0, catalog, ["MATH 18", "MATH 20C", "DSC 40B"])
catalog = add_course("CSE 152A", 4.0, catalog, ["MATH 18", "DSC 30", "DSC 80"])
catalog = add_course("CSE 152B", 4.0, catalog, ["CSE 152A"])
catalog = add_course("CSE 156", 4.0, catalog, ["DSC 40B", "DSC 80", "ECON 120A"]) # TODO fix this
catalog = add_course("CSE 166", 4.0, catalog, ["DSC 40B", "DSC 80"])
catalog = add_course("LIGN 167", 4.0, catalog, ["MATH 20C"])

template = ca.read_csv("./files/SY-Curriculum Plan-DS25.csv")

# business analytics
ba = [(1, ["ECON 1"]), (1, ["ECON 3"]), (5, ["ECON 120B", "ECON 120C", "MATH 152", "MATH 173A", "MATH 173B", "MATH 180A", "MATH 180B", "MATH 180C", "MATH 181A", "MATH 181B", "MATH 181C", "MATH 181D", "MATH 181E", "MATH 181F", "MATH 194", "MGT 103", "MGT 153"])]

science = [(1, ["BILD 1"]), (1, ["BILD 3"]), (5, ["BICD 100", "BIEB 174", "SIO 132", "SIO 109", "POLI 117", "ESYS 103", "COGS 180", "CSE 180", "PSYC 106"])]

social_science1 = [(1, ["POLI 5"]), (1, ["POLI 30"]), (5, ["COMM 106I", "PHIL 174", "POLI 170A", "POLI 171", "POLI 172", "POLI 173", "SOCI 102", "SOCI 103M", "SOCI 108", "SOCI 109", "SOCI 109M", "SOCI 136", "SOCI 165", "SOCI 171", "USP 122", "USP 125", "USP 138","USP 153", "USP 172", "USP 175", "USP 180"])]
social_science2 = [(1, ["SOCI 60"]), (1, ["USP 4"]), (5, ["COMM 106I", "PHIL 174", "POLI 170A", "POLI 171", "POLI 172", "POLI 173", "SOCI 102", "SOCI 103M", "SOCI 108", "SOCI 109", "SOCI 109M", "SOCI 136", "SOCI 165", "SOCI 171", "USP 122", "USP 125", "USP 138","USP 153", "USP 172", "USP 175", "USP 180"])]

ml = [(1, ["COGS 14A"]), (1, ["COGS 14B"]), (5, ["COGS 108", "COGS 109", "COGS 118C", "COGS 118D", "COGS 120", "CSE 170", "COGS 121", "COGS 181", "CSE 151B", "COGS 189", "CSE 106", "CSE 152A", "CSE 152B", "CSE 156", "CSE 166", "LIGN 167"])]

(ba_courses_min, ba_curr_min) = cs.min_complexity(template, ba, catalog)
(ba_courses_max, ba_curr_max) = cs.max_complexity(template, ba, catalog)

(science_courses_min, science_curr_min) = cs.min_complexity(template, science, catalog)
(science_courses_max, science_curr_max) = cs.max_complexity(template, science, catalog)

(social_science1_courses_min, social_science1_curr_min) = cs.min_complexity(template, social_science1, catalog)
(social_science1_courses_max, social_science1_curr_max) = cs.max_complexity(template, social_science1, catalog)

(social_science2_courses_min, social_science2_curr_min) = cs.min_complexity(template, social_science2, catalog)
(social_science2_courses_max, social_science2_curr_max) = cs.max_complexity(template, social_science2, catalog)

(ml_courses_min, ml_curr_min) = cs.min_complexity(template, ml, catalog)
(ml_courses_max, ml_curr_max) = cs.max_complexity(template, ml, catalog)

rand_l = [(2, ["BILD 1", "BILD 3", "POLI 5", "POLI 30", "SOCI 60", "USP 4", "ECON 1", "ECON 3", "COGS 14A", "COGS 14B"])]
rand_u = [(5, ["BICD 100", "BIEB 174", "SIO 132", "SIO 109", "POLI 117", "ESYS 103", "COGS 180", "CSE 180", "PSYC 106", "COMM 106I", "PHIL 174", "POLI 170A", "POLI 171", "POLI 172", "POLI 173", "SOCI 102", "SOCI 103M", "SOCI 108", "SOCI 109", "SOCI 109M", "SOCI 136", "SOCI 165", "SOCI 171", "USP 122", "USP 125", "USP 138", "USP 153", "USP 172", "USP 175", "USP 180", "ECON 120B", "ECON 120C", "MATH 152","MATH 173A", "MATH 173B", "MATH 180A", "MATH 180B", "MATH 180C", "MATH 181A", "MATH 181B", "MATH 181C", "MATH 181D", "MATH 181E", "MATH 181F", "MATH 194", "MGT 103", "MGT 153", "COGS 108", "COGS 109", "COGS 118C", "COGS 118D", "COGS 120", "CSE 170", "COGS 121", "COGS 181", "CSE 151B", "COGS 189", "CSE 106", "CSE 152A", "CSE 152B", "CSE 156", "CSE 166", "LIGN 167"])]

(rand_courses_max, rand_curr_max) = cs.max_complexity(template, rand_l+rand_u, catalog)

complexities_max = [ba_curr_max.metrics["complexity"], science_curr_max.metrics["complexity"], social_science1_curr_max.metrics["complexity"], social_science2_curr_max.metrics["complexity"], ml_curr_max.metrics["complexity"]]
complexities_min = [ba_curr_min.metrics["complexity"], science_curr_min.metrics["complexity"], social_science1_curr_min.metrics["complexity"], social_science2_curr_min.metrics["complexity"], ml_curr_min.metrics["complexity"]]
delays = [max(ba_curr_max.metrics["delay factor"][1]), max(science_curr_max.metrics["delay factor"][1]), max(social_science1_curr_max.metrics["delay factor"][1]), max(social_science2_curr_max.metrics["delay factor"][1]), max(ml_curr_max.metrics["delay factor"][1])]
print("hello")




# this is my manually generated bad curriculum
bad_l = ["USP 4", "ECON 1"]
bad_r = ["MATH 181A", "CSE 150A", "DSC 140B", "DSC 148"] # replacing econ 120a, dsc 140a, dsc 140b, dsc 148 respectively
bad_u = ["COGS 109", "COGS 180", "MATH 152", "CSE 152A", "CSE 152B"]

import copy
dumb_list = copy.deepcopy(template.courses)
#econ120a_index = [c.name for c in dumb_list].index("ECON 120A")
#del dumb_list[econ120a_index]
del dumb_list[[c.name for c in dumb_list].index("DSC 140A")]
new_curr = ca.Curriculum("new", dumb_list, system_type=quarter)
new_curr = cs.add_courses(new_curr, [bad_l + bad_r[0:1] + bad_u], catalog)
new_curr.complexity()[0]
print("hi")