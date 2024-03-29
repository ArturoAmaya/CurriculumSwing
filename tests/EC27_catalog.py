import sys
sys.path.append('./')
import curriculumswing as cs
import curricularanalytics as ca
from curricularanalytics import Course
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


# MATH courses
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


# Physics
catalog = add_course("PHYS 2A",4.0, catalog, ["MATH 20A"])
catalog = add_course("PHYS 2B", 4.0, catalog, ["PHYS 2A", "MATH 20B"])
catalog = add_course("PHYS 2C", 4.0, catalog, ["PHYS 2A", "MATH 20C"])
catalog = add_course("PHYS 2D", 4.0, catalog, ["PHYS 2A", "PHYS 2B", "MATH 20D"])

# COGS
catalog = add_course("COGS 1", 4.0, catalog, [])

c7 = Course("CSE 3", 4.0)
catalog.append(c7)

c8 = Course("CSE 4GS", 4.0)
catalog.append(c8)

c9 = Course("CSE 6GS", 4.0)
c9.add_requisite(c8, "pre")
catalog.append(c9)

c10 = Course("CSE 6R", 4.0)
catalog.append(c10)

c11 = Course("CSE 8A", 4.0)
catalog.append(c11)

c12 = Course("CSE 8B", 4.0)
c12.add_requisite(c11, "pre")
catalog.append(c12)

c13 = Course("CSE 11", 4.0)
catalog.append(c13)

c14 = Course("CSE 12", 4.0)
c14.add_requisite(c13, "pre")
catalog.append(c14)

c15 = Course("CSE 15L", 2.0)
c15.add_requisite(c13, "pre")
catalog.append(c15)

c16 = Course("CSE 20", 4.0)
c16.add_requisite(c13, "pre")
catalog.append(c16)

c17 = Course("CSE 21", 4.0)
c17.add_requisite(c16, "pre")
catalog.append(c17)


c18 = Course("CSE 30", 4.0)
c18.add_requisite(c14, "pre")
c18.add_requisite(c15, "pre")
catalog.append(c18)

c19 = Course("CSE 42", 2.0)
catalog.append(c19)

c20 = Course("CSE 86", 2.0)
c20.add_requisite(c14, "pre")
catalog.append(c20)

c21 = Course("CSE 87", 1.0)
catalog.append(c21)

c22 = Course("CSE 90", 1.0)
catalog.append(c22)

c23 = Course("CSE 91", 2.0)
catalog.append(c23)

c24 = Course("CSE 95", 2.0)
catalog.append(c24)

c25 = Course("CSE 99", 4.0)
catalog.append(c25)

# ECE LOWER DIV
catalog = add_course("ECE 5", 4.0, catalog, [])

catalog = add_course("ECE 15", 4.0, catalog, [])

catalog = add_course("ECE 16", 4.0, catalog, ["CSE 11"]) # or CSE 8B or ECE 15

catalog = add_course("ECE 17", 4.0, catalog, ["CSE 11"])

catalog = add_course("ECE 25", 4.0, catalog, [])

catalog = add_course("ECE 30", 4.0, catalog, ["ECE 15", "ECE 25"])

catalog = add_course("ECE 35", 4.0, catalog, ["MATH 18", "MATH 20A", "MATH 20B", "PHYS 2A"])

catalog = add_course("ECE 45", 4.0, catalog, ["ECE 35"])

catalog = add_course("ECE 65", 4.0, catalog, ["ECE 35"])

catalog = add_course("ECE 85", 4.0, catalog, [])

catalog = add_course("ECE 87", 1.0, catalog, [])

catalog = add_course("ECE 90", 1.0, catalog, [])


# UPPER DIV

#a few ECE needed here
catalog = add_course("ECE 100", 4.0, catalog, ["ECE 45", "ECE 65"])
catalog = add_course("ECE 101", 4.0, catalog, ["ECE 45"])
catalog = add_course("ECE 102", 4.0, catalog, ["ECE 65", "ECE 100"])
catalog = add_course("ECE 103", 4.0, catalog, ["ECE 65", "PHYS 2D"])
catalog = add_course("ECE 107", 4.0, catalog, ["PHYS 2A", "PHYS 2B", "PHYS 2C", "ECE 45"])

catalog = add_course("ECE 109", 4.0, catalog, ["MATH 20A", "MATH 20B", "MATH 20D", "MATH 20C", "MATH 18"])

catalog = add_course("ECE 115", 4.0,  catalog, ["ECE 16"])
catalog = add_course("ECE 118", 4.0, catalog, ["CSE 30", "ECE 35", "ECE 45", "ECE 65"])
catalog = add_course("ECE 121A", 4.0, catalog, ["ECE 35"])
catalog = add_course("ECE 121B", 4.0, catalog, ["ECE 121A"])
catalog = add_course("ECE 123", 4.0, catalog, ["ECE 107"])
catalog = add_course("ECE 125A", 4.0, catalog, ["ECE 121A"])
catalog = add_course("ECE 124", 4.0, catalog, ["ECE 121B", "ECE 125A"])

catalog = add_course("ECE 125B", 4.0, catalog, ["ECE 125A"])
catalog = add_course("ECE 128A", 4.0, catalog, [])
catalog = add_course("ECE 128B", 4.0, catalog, ["ECE 35", "ECE 128A"])
catalog = add_course("ECE 128C", 4.0, catalog, [ "ECE 128B"])
catalog = add_course("ECE 129", 4.0, catalog, [])
catalog = add_course("ECE 134", 4.0, catalog, ["PHYS 2C", "PHYS 2D"])
catalog = add_course("ECE 135A", 4.0, catalog, ["ECE 103"])
catalog = add_course("ECE 135B", 4.0, catalog, ["ECE 135A"])
catalog = add_course("ECE 136L", 4.0, catalog, ["ECE 135B"])
catalog = add_course("ECE 138L", 4.0, catalog, [])
catalog = add_course("ECE 139" ,4.0, catalog, [])
catalog = add_course("ECE 140A", 4.0, catalog, ["CSE 11"])
catalog = add_course("ECE 140B", 4.0, catalog, ["ECE 140A"])
catalog = add_course("ECE 141A", 4.0, catalog, ["ECE 17", "CSE 30"])
catalog = add_course("ECE 141B", 4.0, catalog, ["ECE 141A"])
catalog = add_course("ECE 143", 4.0, catalog, ["ECE 16"])
catalog = add_course("ECE 144", 4.0, catalog, ["CSE 11"])
catalog = add_course("ECE 145AL", 4.0, catalog, ["ECE 107"])
catalog = add_course("ECE 145BL", 4.0, catalog, ["ECE 145AL"])
catalog = add_course("ECE 145CL", 4.0, catalog, ["ECE 145BL"])
catalog = add_course("ECE 148", 4.0, catalog, ["ECE 35"])
catalog = add_course("ECE 150", 4.0, catalog, [])
catalog = add_course("ECE 153", 4.0, catalog, ["ECE 109"])
catalog = add_course("ECE 155", 4.0, catalog, ["ECE 101", "ECE 109", "ECE 153"])
catalog = add_course("ECE 156", 4.0, catalog, [])
catalog = add_course("ECE 158A", 4.0, catalog, ["ECE 109"])
catalog = add_course("ECE 158B", 4.0, catalog, ["ECE 158A"])
catalog = add_course("ECE 159", 4.0, catalog, ["ECE 153"])
catalog = add_course("ECE 161A", 4.0, catalog, ["ECE 101"])
catalog = add_course("ECE 157A", 4.0, catalog, ["ECE 109", "ECE 161A"])
catalog = add_course("ECE 157B", 4.0, catalog, ["ECE 157A"])

catalog = add_course("ECE 161B", 4.0, catalog, ["ECE 161A"])
catalog = add_course("ECE 161C", 4.0, catalog, ["ECE 161A"])
catalog = add_course("ECE 163", 4.0, catalog, ["ECE 101", "ECE 102"])
catalog = add_course("ECE 164", 4.0, catalog, ["ECE 102"])
catalog = add_course("ECE 165", 4.0, catalog, ["ECE 102"])
catalog = add_course("ECE 166", 4.0, catalog, ["ECE 102", "ECE 107"])
catalog = add_course("ECE 171A", 4.0, catalog, ["ECE 45"])
catalog = add_course("ECE 171B", 4.0, catalog, ["ECE 171A"])
catalog = add_course("ECE 172A", 4.0, catalog, ["ECE 101"])
catalog = add_course("ECE 174", 4.0, catalog, ["MATH 18", "ECE 15"])
catalog = add_course("ECE 175A", 4.0, catalog, ["ECE 109", "ECE 174"])
catalog = add_course("ECE 175B", 4.0, catalog, ["ECE 175A"])
catalog = add_course("ECE 176", 4.0, catalog, ["MATH 18"])
catalog = add_course("ECE 180", 4.0, catalog, [])
catalog = add_course("ECE 181", 4.0, catalog, ["ECE 103", "ECE 107"])
catalog = add_course("ECE 182", 4.0, catalog, ["ECE 103", "ECE 107"])
catalog = add_course("ECE 183", 4.0, catalog, ["ECE 103", "ECE 107"])
catalog = add_course("ECE 184", 4.0, catalog, ["ECE 182"])
catalog = add_course("ECE 185", 4.0, catalog, ["ECE 183"])
catalog = add_course("ECE 187", 4.0, catalog, ["MATH 20A", "MATH 20B", "MATH 20C", "MATH 20D", "MATH 18", "PHYS 2A", "PHYS 2B", "PHYS 2C", "PHYS 2D", "ECE 101"])
catalog = add_course("ECE 188", 4.0, catalog, [])
catalog = add_course("ECE 189", 2.0, catalog, [])
catalog = add_course("ECE 190", 4.0, catalog, [])
catalog = add_course("ECE 191", 4.0, catalog, [])
catalog = add_course("ECE 193H", 4.0, catalog, [])
catalog = add_course("ECE 194", 4.0, catalog, [])

catalog = add_course("ECE 196", 4.0, catalog, ["CSE 11"])
#catalog = add_course("ECE 197", 12.0, catalog, [])
#catalog = add_course("ECE 198", 4.0, catalog, [])
#catalog = add_course("ECE 199", 4.0, catalog, [])

c26 = Course("CSE 100", 4.0)
c26.add_requisite(c17, "pre") # CSE 21
c26.add_requisite(c14, "pre") # CSE 12
c26.add_requisite(c15, "pre") # CSE 15L
c26.add_requisite(c18, "pre") # CSE 30
catalog.append(c26)

c27 = Course("CSE 101", 4.0)
c27.add_requisite(c17, "pre")
c27.add_requisite(c14, "pre")
catalog.append(c27)

c28 = Course("CSE 103", 4.0)
c28.add_requisite(c2, "pre")
c28.add_requisite(course_find("CSE 21", catalog), "pre")
catalog.append(c28)

c29 = Course("CSE 105", 4.0)
c29.add_requisite(course_find("CSE 12", catalog), "pre")
c29.add_requisite(course_find("CSE 15L", catalog), "pre")
c29.add_requisite(course_find("CSE 20", catalog), "pre")
c29.add_requisite(course_find("CSE 21", catalog), "pre")
catalog.append(c29)


catalog = add_course("CSE 106", 4.0, catalog, ["MATH 18", "MATH 20C", "CSE 21"])

catalog = add_course("CSE 107", 4.0, catalog, ["CSE 21", "CSE 101", "CSE 105"])

catalog = add_course("CSE 109", 4.0, catalog, ["CSE 30"])

catalog = add_course("CSE 110", 4.0, catalog, ["CSE 100"])

catalog = add_course("CSE 112", 4.0, catalog, ["CSE 110"])

#catalog = add_course("CSE 118", 4.0, catalog, ["ECE 111"]) # it's a bunch of ORs
#TODO add ECE catalog
catalog = add_course("CSE 120", 4.0, catalog, ["CSE 30", "CSE 101", "CSE 110"])

catalog = add_course("CSE 123", 4.0, catalog, ["CSE 30", "CSE 101", "CSE 110"])

catalog = add_course("CSE 124", 4.0, catalog, ["CSE 30", "CSE 101", "CSE 110"])

catalog = add_course("CSE 125", 4.0, catalog, [])

catalog = add_course("CSE 127", 4.0, catalog, ["CSE 30"])

catalog = add_course("CSE 130", 4.0, catalog, ["CSE 12", "CSE 100", "CSE 105"])

catalog = add_course("CSE 131", 4.0, catalog, ["CSE 100", "CSE 105", "CSE 130"])

catalog = add_course("CSE 132A", 4.0, catalog, ["CSE 100"])

catalog = add_course("CSE 132B", 4.0, catalog, ["CSE 132A"])

catalog = add_course("CSE 132C", 4.0, catalog, ["CSE 132A"])

catalog = add_course("CSE 134B", 4.0, catalog, ["CSE 100"])

catalog = add_course("CSE 135", 4.0, catalog, ["CSE 100"])

catalog = add_course("CSE 136", 4.0, catalog, ["CSE 135"])

catalog = add_course("CSE 140", 4.0, catalog, ["CSE 20", "CSE 30"])
catalog = add_course("ECE 108", 4.0, catalog, ["CSE 140", "ECE 45", "ECE 65", "CSE 30"])
catalog = add_course("ECE 111", 4.0, catalog, ["CSE 140"])

catalog = add_course("CSE 140L", 2.0, catalog, ["CSE 20", "CSE 30"])

catalog = add_course("CSE 141", 4.0, catalog, ["CSE 30", "CSE 140", "CSE 140L"])

catalog = add_course("CSE 141L", 2.0, catalog, ["CSE 30", "CSE 140", "CSE 140L"])

catalog = add_course("CSE 142", 4.0, catalog, ["CSE 30", "CSE 100"])

catalog = add_course("CSE 142L", 2.0, catalog, ["CSE 30", "CSE 100"])

catalog = add_course("CSE 143", 4.0, catalog, ["CSE 140"])

catalog = add_course("CSE 145", 4.0, catalog, [])

catalog = add_course("CSE 148", 4.0, catalog, ["CSE 141", "CSE 141L"])

catalog = add_course("CSE 150A", 4.0, catalog, ["CSE 12", "CSE 15L"])

catalog = add_course("CSE 150B", 4.0, catalog, ["CSE 12", "CSE 15L", "ECE 109", "CSE 100"])

catalog = add_course("CSE 151A", 4.0, catalog, ["CSE 12", "CSE 15L", "ECE 109", "MATH 18", "MATH 20C"])

catalog = add_course("CSE 151B", 4.0, catalog, ["MATH 20C", "ECE 109"])

catalog = add_course("CSE 152A", 4.0, catalog, ["MATH 18", "CSE 12", "CSE 15L"])

catalog = add_course("CSE 152B", 4.0, catalog, ["CSE 152A"])

catalog = add_course("CSE 156", 4.0, catalog, ["CSE 12", "CSE 15L", "ECE 109"])

catalog = add_course("CSE 158", 4.0, catalog, ["CSE 12", "CSE 15L", "ECE 109"])

catalog = add_course("CSE 160", 4.0, catalog, ["CSE 100"])

catalog = add_course("CSE 167", 4.0, catalog, ["CSE 100"])

catalog = add_course("CSE 163", 4.0, catalog, ["CSE 167"])

catalog = add_course("CSE 165", 4.0, catalog, ["CSE 167"])

catalog = add_course("CSE 166", 4.0, catalog, ["MATH 18", "CSE 100"])

catalog = add_course("CSE 168", 4.0, catalog, ["CSE 167"])

catalog = add_course("CSE 169", 4.0, catalog, ["CSE 167"])

catalog = add_course("CSE 170", 4.0, catalog, ["CSE 12", "COGS 1"])

catalog = add_course("CSE 175", 4.0, catalog, [])

catalog = add_course("CSE 176A", 4.0, catalog, ["CSE 110"])

catalog = add_course("CSE 176E", 4.0, catalog, [])

catalog = add_course("CSE 180", 4.0, catalog, [])

#catalog = add_course("CSE 181", 4.0, catalog, ["CSE 100", "CSE 101", "BIMM 100"])
# wrong major
#catalog = add_course("CSE 182", 4.0, catalog, ["CSE 100"])

#catalog = add_course("CSE 184", 4.0, catalog)
# wrong major

# cse 185 is also wrong major

catalog = add_course("CSE 190", 4.0, catalog, [])

# skip 191

catalog = add_course("CSE 192", 1.0, catalog, [])

catalog = add_course("CSE 193", 4.0, catalog, [])

catalog = add_course("CSE 194", 1.0, catalog, ["CSE 12"]) # or a college writing course but screw that for now])

# CSE 195 doesn't count
#catalog = add_course("CSE 197", 4.0, catalog, [])
#catalog = add_course("CSE 197C" ,12.0, catalog, [])
#catalog = add_course("CSE 198", 4.0, catalog, [])
#catalog = add_course("CSE 199", 4.0, catalog, [])
#catalog = add_course("CSE 199H", 4.0, catalog, [])

# LDE
catalog = add_course("MAE 8", 4.0, catalog, ["MATH 20A", "MATH 20B"])
catalog = add_course("MAE 9", 4.0, catalog, [])
catalog = add_course("COGS 9", 4.0, catalog, [])
catalog = add_course("COGS 10", 4.0, catalog, [])
catalog = add_course("COGS 18", 4.0, catalog, [])
catalog = add_course("NANO 15", 4.0, catalog, [])
catalog = add_course("CENG 15", 4.0, catalog, [])

# NOTE: This does NOT include the extra non-CSE/ECE electives that are available to a EC26 major

upper_div_eng = ["ECE 100", "ECE 101", "ECE 102", "ECE 103", "ECE 107", 
                 "ECE 109", "ECE 115", "ECE 118", "ECE 121A",
                 "ECE 121B", "ECE 123", "ECE 125A", "ECE 124", "ECE 125B", 
                 "ECE 128A", "ECE 128B", "ECE 128C",
                 "ECE 129", "ECE 134", "ECE 135A", "ECE 135B", "ECE 136L", 
                 "ECE 138L", "ECE 139", "ECE 140A",
                 "ECE 140B", "ECE 141A", "ECE 141B", "ECE 143", "ECE 144", 
                 "ECE 145AL", "ECE 145BL", "ECE 145CL", "ECE 148",
                 "ECE 150", "ECE 153", "ECE 155", "ECE 156", "ECE 158A",
                 "ECE 158B", "ECE 159", "ECE 161A", "ECE 157A", "ECE 157B", 
                 "ECE 161B", "ECE 161C", "ECE 163", "ECE 164", "ECE 165",
                 "ECE 166", "ECE 171A", "ECE 171B", "ECE 172A", "ECE 174", "ECE 175A",
                 "ECE 175B", "ECE 176", "ECE 180", "ECE 181", "ECE 182", "ECE 183",
                 "ECE 185", "ECE 187", "ECE 188", "ECE 189", "ECE 190", "ECE 191",
                 "ECE 193H", "ECE 194", "ECE 196",
                 "CSE 100", "CSE 101", "CSE 103", "CSE 105", "CSE 106","CSE 107",
                 "CSE 109", "CSE 110", "CSE 112", "CSE 120", "CSE 123", "CSE 124", 
                 "CSE 125", "CSE 127", "CSE 130", "CSE 131", "CSE 132A", "CSE 132B",
                 "CSE 132C", "CSE 134B", "CSE 135", "CSE 136", "CSE 140", "ECE 108",
                 "ECE 111", "CSE 140L", "CSE 141", "CSE 141L", "CSE 142", "CSE 142L",
                 "CSE 143", "CSE 145", "CSE 148", "CSE 150A", "CSE 150B", "CSE 151A",
                 "CSE 151B", "CSE 152A", "CSE 152B", "CSE 156", "CSE 158", "CSE 160",
                 "CSE 167", "CSE 163", "CSE 165", "CSE 166", "CSE 168", "CSE 169", "CSE 170",
                 "CSE 175", "CSE 176A", "CSE 176E", "CSE 180", "CSE 190", "CSE 192", "CSE 193",
                 "CSE 194"]

template = ca.read_csv("./files/SY-Curriculum Plan-EC27.csv")

# design the elective sequences
# Communication Systems
comm_electives = [(1, ["ECE 100"]), (1, ["ECE 101"]), (1, ["ECE 102"]), (1, ["ECE 107"]), (1, ["ECE 109"]), (1, ["ECE 153"]), (1, ["ECE 155"]), (1, ["ECE 157A"]), (1, ["ECE 158A"]), (1, ["ECE 159"])]
comm_electives.append((4, upper_div_eng))
comm_electives.append((2, upper_div_eng))
comm_electives.append((1, ["ECE 111", "ECE 115", "ECE 140B", "ECE 190", "ECE 191"]))

(comm_courses_min, comm_curr_min) = cs.min_complexity(template, comm_electives, catalog)
(comm_courses_max, comm_curr_max) = cs.max_complexity(template, comm_electives, catalog)


# Computer System Design
comp_design = [(1, ["ECE 100"]), (1, ["ECE 101"]), (1, ["ECE 109"])]
comp_design.append((5, ["ECE 102", "ECE 103", "ECE 111", "ECE 140A",
                        "ECE 140B", "ECE 141A", "ECE 141B",
                        "ECE 143", "ECE 158A", "ECE 158B", "ECE 165"]))
comp_design.append((5, upper_div_eng))
comp_design.append((2, upper_div_eng))
comp_design.append((1, ["ECE 111", "ECE 115", "ECE 140B", "ECE 190", "ECE 191"]))

(comp_design_min, comp_design_curr_min) = cs.min_complexity(template, comp_design, catalog)
(comp_design_courses_max, comp_design_curr_max) = cs.max_complexity(template, comp_design, catalog)

# Electronic Circuits and Systems
ecs = [(1, ["ECE 100"]), (1, ["ECE 101"]), (1, ["ECE 102"]), (1, ["ECE 103"]), (1, ["ECE 107"]), (1, ["ECE 109"])]
ecs.append((1, ["ECE 164"]))
ecs.append((1, ["ECE 165"]))
ecs.append((1, ["ECE 166"]))
ecs.append((5, upper_div_eng))
ecs.append((2, upper_div_eng))
ecs.append((1, ["ECE 111", "ECE 115", "ECE 140B", "ECE 190", "ECE 191"]))

(ecs_courses_min, ecs_curr_min) = cs.min_complexity(template, ecs, catalog)
(ecs_courses_max, ecs_curr_max) = cs.max_complexity(template, ecs, catalog)


# Electronics Devices and Materials
edm = [(1, ["ECE 100"]), (1, ["ECE 101"]), (1, ["ECE 102"]), (1, ["ECE 103"]), (1, ["ECE 107"]), (1, ["ECE 109"])]
edm.append((1, ["ECE 135A"]))
edm.append((1, ["ECE 135B"]))
edm.append((1, ["ECE 136L"]))
edm.append((1, ["ECE 183"]))
edm.append((5, upper_div_eng))
edm.append((2, upper_div_eng))
edm.append((1, ["ECE 111", "ECE 115", "ECE 140B", "ECE 190", "ECE 191"]))

(edm_courses_min, edm_curr_min) = cs.min_complexity(template, edm, catalog)
(edm_courses_max, edm_curr_max) = cs.max_complexity(template, edm, catalog)

# Machine Learning and Controls
mlc = [(1, ["ECE 100"]), (1, ["ECE 101"]), (1, ["ECE 107"]), (1, ["ECE 109"])]
mlc.append((1, ["ECE 171A"]))
mlc.append((1, ["ECE 174"]))
mlc.append((1, ["ECE 175A"]))
mlc.append((1, ["ECE 171B", "ECE 172A", "ECE 175B"]))
mlc.append((6, upper_div_eng))
mlc.append((2, upper_div_eng))
mlc.append((1, ["ECE 111", "ECE 115", "ECE 140B", "ECE 190", "ECE 191"]))

(mlc_courses_min, mlc_curr_min) = cs.min_complexity(template, mlc, catalog)
(mlc_courses_max, mlc_curr_max) = cs.max_complexity(template, mlc, catalog)

# Photonics
photonics = [(1, ["ECE 100"]), (1, ["ECE 101"]), (1, ["ECE 103"]), (1, ["ECE 107"]), (1, ["ECE 109"])]
photonics.append((1, ["ECE 181"]))
photonics.append((1, ["ECE 182"]))
photonics.append((1, ["ECE 183"]))
photonics.append((1, ["ECE 184", "ECE 185"]))

(photonics_courses_min, photonics_curr_min) = cs.min_complexity(template, photonics, catalog)
(photonics_courses_max, photonics_curr_max) = cs.max_complexity(template, photonics, catalog)


# Power Engineering
pe = [(1, ["ECE 100"]), (1, ["ECE 101"]), (1, ["ECE 102"]), (1, ["ECE 103"]), (1, ["ECE 107"]), (1,["ECE 109"])]
pe.append((1, ["ECE 121A"]))
pe.append((1, ["ECE 121B"]))
pe.append((1, ["ECE 125A"]))
pe.append((1, ["ECE 128A"]))
pe.append((1, ["ECE 125B", "ECE 128B"]))
pe.append((3, upper_div_eng))
pe.append((2, upper_div_eng))
pe.append((1, ["ECE 111", "ECE 115", "ECE 140B", "ECE 190", "ECE 191"]))

(pe_courses_min, pe_curr_min) = cs.min_complexity(template, pe, catalog)
(pe_courses_max, pe_curr_max) = cs.max_complexity(template, pe, catalog)


# Signal and Image Processing
sip = [(1, ["ECE 100"]), (1, ["ECE 101"]), (1, ["ECE 107"]), (1, ["ECE 109"])]
sip.append((1, ["ECE 153"]))
sip.append((1, ["ECE 161A"]))
sip.append((1, ["ECE 161B"]))
sip.append((1, ["ECE 161C"]))
sip.append((6, upper_div_eng))
sip.append((2, upper_div_eng))
sip.append((1, ["ECE 111", "ECE 115", "ECE 140B", "ECE 190", "ECE 191"]))

(sip_courses_min, sip_curr_min) = cs.min_complexity(template, sip, catalog)
(sip_courses_max, sip_curr_max) = cs.max_complexity(template, sip, catalog)

complexities_max = [comm_curr_max.metrics["complexity"], comp_design_curr_max.metrics["complexity"], ecs_curr_max.metrics["complexity"], edm_curr_max.metrics["complexity"], mlc_curr_max.metrics["complexity"],photonics_curr_max.metrics["complexity"],pe_curr_max.metrics["complexity"], sip_curr_max.metrics["complexity"]]
complexities_min = [comm_curr_min.metrics["complexity"], comp_design_curr_min.metrics["complexity"], ecs_curr_min.metrics["complexity"], edm_curr_min.metrics["complexity"], mlc_curr_min.metrics["complexity"],photonics_curr_min.metrics["complexity"],pe_curr_min.metrics["complexity"], sip_curr_min.metrics["complexity"]]

print("hello")