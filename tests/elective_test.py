import sys
sys.path.append('./')
from curriculumswing import Elective
from curricularanalytics import Course, Curriculum
# make some courses
c1 = Course("MATH 20A", 4.0)
c2 = Course("MATH 20B", 4.0)
c2.add_requisite(c1, 'pre')
c3 = Course("MATH 20C", 4.0)
c3.add_requisite(c2, 'pre')
c4 = Course("MATH 20D", 4.0)
c4.add_requisite(c3, 'pre')
c5 = Course("MATH 20E", 4.0)
c5.add_requisite(c4, 'pre')
c6 = Course("MATH 18", 4.0)
c5.add_requisite(c6, 'pre')

# make an elective normally
c7 = Course("TE 1", 4.0)

# these are the elective courses
e1 = Course("CSE 101", 4.0)
e1.add_requisite(c5, 'pre')
e2 = Course("CSE 110", 4.0)
e2.add_requisite(c5, 'pre')
e3 = Course("CSE 114", 4.0)
e3.add_requisite(c5, 'pre')


# make an inactive elective
E1 = Elective("TE 1", [e1,e2,e3], 2, False)

# make a curriculum with the inactive elective and check complexity
C1 = Curriculum("C 1", [c1, c2, c3, c4, c5, c6, E1])
C1.basic_metrics()
print(C1.complexity())
print(C1.courses[0].name, C1.courses[0].metrics["complexity"])
print(C1.courses[1].name, C1.courses[1].metrics["complexity"])
print(C1.courses[2].name, C1.courses[2].metrics["complexity"])