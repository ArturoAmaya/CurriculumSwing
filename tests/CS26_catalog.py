import sys
sys.path.append('./')
import curriculumswing as cs
import curricularanalytics as ca
from curricularanalytics import Course, quarter
from typing import List, OrderedDict
from curricularanalytics import DegreePlan, Term
import random
from curricularanalytics import pre, Curriculum
from curriculumswing import add_courses, add_course
import re 
import urllib 

def course_check(course:Course, terms):
    found = False
    term_id = 0
    for term in terms:
        if course in term:
            found = True
            term_id = terms.index(term)
            break
    return found, term_id

def dp_ize(curr: Curriculum, base: DegreePlan):
    # somehow make terms from the curriculum
    terms = [[] for i in range(12)]
    index=0
    l = []

    # add in all the courses from the base plan
    for base_term in base.terms:
        for base_course in base_term.courses:
            for course in curr.courses:
                if base_course.name == course.name or (base_course.prefix + ' ' + base_course.num == course.name):
                    terms[base.terms.index(base_term)].append(course)
    
    # insert remaining courses such that they are after their prerequisites
    for course in curr.courses:
        found = course_check(course, terms)[0]
        if found:
            continue

        # if it's not already there continue
        # want to add course after all of its prerequisites

        # first thing add the ones with no prerequisites
        
        if not course.requisites: # ie. no prerequisites

            # this syntax is pretty brittle, may fail haven't tested enough
            idx = 0 if int(''.join(c for c in course.name.split(" ")[-1] if not c.isalpha())) < 99 else 6 # 2 years before upper divs are allowed
            for term in terms[idx:]:
                if sum([course.credit_hours for course in term]) < 20:
                    term.append(course)
                    break
        else:
            max_preq = 0
            # make sure it goes in after its prerequisites
            for key, value in course.requisites.items():
                pred_id = key
                
                found, term_id = course_check([c for c in curr.courses if c.id==key][0], terms)
                if not found:
                    # add that course in
                    print("yikes")
                else:
                    if term_id > max_preq:
                        max_preq = term_id
            
            if int(''.join(c for c in course.name.split(" ")[-1] if not c.isalpha())) < 99:
                idx = max_preq + 1
            else:
                if max_preq > 5:
                    idx = max_preq + 1
                else: 
                    idx = 6
            for term in terms[idx:]:
                if sum([course.credit_hours for course in term]) < 20:
                    term.append(course)
                    break




    dp_max = DegreePlan('cs26 max', curr, [Term(term) for term in terms])
    return dp_max

def urlize(dp:DegreePlan, college: str, major:str, year:int, optimized: bool, ruleset: str=None):
    c = ca.write_csv(dp, '', iostream=True) # if you don't say where it writes to string
    d = re.sub('"([a-z, A-Z,0-9]+[\/,0-9,A-Z, ]+)"', r'\1', c.getvalue())
    shard = urllib.parse.quote(re.sub('"(([0-9]+;?)*)"', r'\1', d), safe='()/')
    # new content in the url includes year, major code, title
    title = f"&title={major}+({college},+{year}):+{(dp.curriculum.name).replace(' ', '+')}"
    year = f"&year={year}"
    major = f"&major={major}"
    #title = f"&title={major}+({college},+{2024}):+{(dp.curriculum.name).replace(' ', '+')}"
    #&year=2024&major=PB31&title=PB31+(Revelle,+2024):+Public+Health+with+Concentration+in+Medicine+Sciences
    dp_url = "https://educationalinnovation.ucsd.edu/_files/graph-demo.html?defaults=ucsd" + year + major + title + "#" + shard
    return dp_url

#########################
# Markdown Report generator
def markdown_gen(data, filename="report.md"):
    with open(filename, 'w') as f:
        f.write("# MinMax analysis for CS26\n\n")
        for section in data:
            f.write(f"## {section["section"]}\n\n")

            results = section["results"]
            # write the results
            f.write(f"### template\n\n")
            f.write(f"[visualize]({results['template']["url"]})\n")
            f.write(f"complexity: {results['template']['complexity'][0]}\n")
            f.write(f"centrality: {results['template']['centrality'][0]}\n")

            f.write(f"### max\n\n")
            f.write(f"[visualize]({results['max']["url"]})\n")
            f.write(f"complexity: {results['max']['complexity'][0]}\n")
            f.write(f"centrality: {results['max']['centrality'][0]}\n")

            f.write(f"### min\n\n")
            f.write(f"[visualize]({results['min']["url"]})\n")
            f.write(f"complexity: {results['min']['complexity'][0]}\n")
            f.write(f"centrality: {results['min']['centrality'][0]}\n")



#########################
# CATALOG

catalog = []
def course_find(name:str, li:List[Course])->Course:
    for course in li:
        if course.name == name:
            return course

def add_course2catalog(name:str, units:float, catalog:List[Course], prereq_names:List[str]):
    c = Course(name, units)
    for preq in prereq_names:
        c.add_requisite(course_find(preq, catalog), pre)
    catalog.append(c)
    return catalog
def id_generator(start=1):
    while True:
        yield start
        start += 1

id_gen = id_generator()

# MATH courses
c1 = Course("MATH 20A", 4.0, id=next(id_gen))
catalog.append(c1)
c2 = Course("MATH 20B", 4.0, id=next(id_gen))
c2.add_requisite(c1, pre)
catalog.append(c2)
c3 = Course("MATH 18", 4.0, id=next(id_gen))
catalog.append(c3)
c4 = Course("MATH 20C", 4.0, id=next(id_gen))
c4.add_requisite(c2, pre)
catalog.append(c4)
c5 = Course("MATH 20D", 4.0, id=next(id_gen))
c5.add_requisite(c4, pre)
catalog.append(c5)
c6 = Course("MATH 20E", 4.0, id=next(id_gen))
c6.add_requisite(c5, pre)
c6.add_requisite(c3, pre)
catalog.append(c6)

# ECE 109
ece109 = Course("ECE 109", 4.0, id=next(id_gen))
ece109.add_requisite(c1, pre)
ece109.add_requisite(c2, pre)
ece109.add_requisite(c3, pre)
ece109.add_requisite(c4, pre)
ece109.add_requisite(c5, pre)
catalog.append(ece109)

# CSE Lower Div Courses
cse8a = Course("CSE 8A", 4.0, id=next(id_gen))
catalog.append(cse8a)

cse8b = Course("CSE 8B", 4.0, id=next(id_gen))
cse8b.add_requisite(cse8a, pre)
catalog.append(cse8b)

cse11 = Course("CSE 11", 4.0, id=next(id_gen))
catalog.append(cse11)

cse20 = Course("CSE 20", 4.0, id=next(id_gen))
cse20.add_requisite(cse8b, pre) # or 8B or 8A TODO
catalog.append(cse20)

math109 = Course("MATH 109", 4.0, id=next(id_gen))
math109.add_requisite(c3, pre)
math109.add_requisite(c4, pre)
catalog.append(math109)

math154 = Course("MATH 154", 4.0, id=next(id_gen))
math154.add_requisite(math109, pre)
catalog.append(math154)

math184 = Course("MATH 184", 4.0, id=next(id_gen))
math184.add_requisite(math109, pre)
catalog.append(math184)

# MATH 181A
math180a = Course("MATH 180A", 4.0, id=next(id_gen))
math180a.add_requisite(c4, pre)
catalog.append(math180a)
math181a = Course("MATH 181A", 4.0, id=next(id_gen))
math181a.add_requisite(math180a, pre)
math181a.add_requisite(c3, pre)
math181a.add_requisite(c4, pre)
catalog.append(math181a)

# MATH 183
math183 = Course("MATH 183", 4.0, id=next(id_gen))
math183.add_requisite(c4, pre)
catalog.append(math183)

# MATH 170A,  MATH 170B, MATH 170C, 
math170a = Course("MATH 170A", 4.0, id=next(id_gen))
math170a.add_requisite(c3, pre)
math170a.add_requisite(c4, pre)
math170a.add_requisite(cse20, pre) # or MATH 109
catalog.append(math170a)

math170b = Course("MATH 170B", 4.0, id=next(id_gen))
math170b.add_requisite(math170a, pre)
catalog.append(math170b)

math170c = Course("MATH 170C", 4.0, id=next(id_gen))
math170c.add_requisite(math170b, pre)
math170c.add_requisite(c5, pre)
catalog.append(math170c)


# MATH 171A, MATH 171B, 
math171a = Course("MATH 171A", 4.0, id=next(id_gen))
math171a.add_requisite(c3, pre)
math171a.add_requisite(c4, pre)
catalog.append(math171a)

math171b = Course("MATH 171B", 4.0, id=next(id_gen))
math171b.add_requisite(c4, pre)
math171b.add_requisite(math171a, pre)
catalog.append(math171b)


# MATH 173A, MATH 173B,  
math173a = Course("MATH 173A", 4.0, id=next(id_gen))
math173a.add_requisite(c3, pre)
math173a.add_requisite(c4, pre)
catalog.append(math173a)
math173b = Course("MATH 173B", 4.0, id=next(id_gen))
math173b.add_requisite(math173a, pre)
catalog.append(math173b)

# MATH 181D, 
math181d = Course("MATH 181D", 4.0, id=next(id_gen))
# ECE 109 or ECON 120A or MAE 108 or MATH 181A or MATH 183 or MATH 186 or MATH 189. Students who have not completed listed prerequisites may enroll with consent of instructor.
# TODO
catalog.append(math181d)


# MATH 185,  
math185 = Course("MATH 185", 4.0, id=next(id_gen))
math185.add_requisite(math181a, pre) # or ECON 120B
math185.add_requisite(c3, pre)
math185.add_requisite(c4, pre)
catalog.append(math185)


# MATH 187A
math187a = Course("MATH 187A", 4.0, id=next(id_gen))
math187a.add_requisite(c1, pre)
catalog.append(math187a)


# MATH 114, 
math114 = Course("MATH 114", 4.0, id=next(id_gen))
math114.add_requisite(math180a, pre)
catalog.append(math114)

# MATH 155A, 
math155a = Course("MATH 155A", 4.0, id=next(id_gen))
math155a.add_requisite(c3, pre)
math155a.add_requisite(c4, pre)
catalog.append(math155a)

# MATH 189, 
math189 = Course("MATH 189", 4.0, id=next(id_gen))
math189.add_requisite(c3, pre)
math189.add_requisite(c4, pre)
math189.add_requisite(ece109, pre)
catalog.append(math189)
# TODO: one of BENG 134, CSE 103, ECE 109, ECON 120A, MAE 108, MATH 180A, MATH 183, MATH 186, or SE 125


# CSE Lower Div Courses

cse12 = Course("CSE 12", 4.0, id=next(id_gen))
cse12.add_requisite(cse8b, pre) # going with 8b here for worst case analysis because 8b implies 8a
catalog.append(cse12) # or CSE 8B TODO

cse21 = Course("CSE 21", 4.0, id=next(id_gen))
cse21.add_requisite(cse20, pre)
catalog.append(cse21)

cse29 = Course("CSE 29", 4.0, id=next(id_gen))
cse29.add_requisite(cse8b, pre) # TODO or 8b
catalog.append(cse29)

cse30 = Course("CSE 30", 4.0, id=next(id_gen))
cse30.add_requisite(cse29, pre)
catalog.append(cse30)

cse3 = Course("CSE 3", 4.0, id=next(id_gen))
catalog.append(cse3)

cse4gs = Course("CSE 4GS", 4.0, id=next(id_gen))
cse4gs.add_requisite(c1, pre)
cse6gs = Course("CSE 6GS", 4.0, id=next(id_gen))
cse6gs.add_requisite(c1, pre)
# TODO: double check this syntax and if it even matters for us
catalog.append(cse4gs)
catalog.append(cse6gs)

cse6r = Course("CSE 6R", 4.0, id=next(id_gen))
catalog.append(cse6r)

cse42 = Course("CSE 42", 2.0, id=next(id_gen)) #restricted to first and second-years
catalog.append(cse42)

cse86 = Course("CSE 86", 2.0, id=next(id_gen))
cse86.add_requisite(cse12, pre) # TODO check this and cse42 against the course picking code. they're 2 units among 4 unit classes I think I just say pick classes not pick units
catalog.append(cse86)

cse90 = Course("CSE 90", 1.0, id=next(id_gen))
catalog.append(cse90)

cse91 = Course("CSE 91", 2.0, id=next(id_gen))
catalog.append(cse91)

cse95 = Course("CSE 95", 2.0, id=next(id_gen))
catalog.append(cse95)

cse99 = Course("CSE 99", 4.0, id=next(id_gen))
catalog.append(cse99)

bild1 = Course("BILD 1", 4.0, id=next(id_gen))
catalog.append(bild1)

#### CSE UPPER DIVISION COURSES
cse180 = Course("CSE 180", 4.0, id=next(id_gen))
cse180.add_requisite(bild1, pre) # TODO or BILD 4
cse180.add_requisite(cse8b, pre) # TODO or 8B or 3 or 8A
catalog.append(cse180)
# CSE 180R is a copy of CSE 180 just remote. ignore it 

cse103 = Course("CSE 103", 4.0, id=next(id_gen))
cse103.add_requisite(c2, pre)
cse103.add_requisite(cse21, pre) # or MATH 154 or MATH 184
catalog.append(cse103)

mae8 = Course("MAE 8", 4.0, id=next(id_gen))
mae8.add_requisite(c1, pre)
mae8.add_requisite(c2, pre)
catalog.append(mae8)

mae9 = Course("MAE 9", 4.0, id=next(id_gen)) # DNE

cogs9 = Course("COGS 9", 4.0, id=next(id_gen))
catalog.append(cogs9)

cogs10 = Course("COGS 10", 4.0, id=next(id_gen))
catalog.append(cogs10)

cogs18 = Course("COGS 18", 4.0, id=next(id_gen))
catalog.append(cogs18)


ece15 = Course("ECE 15", 4.0, id=next(id_gen))
catalog.append(ece15)

eng10 = Course("ENG 10", 2.0, id=next(id_gen))
catalog.append(eng10)

eng15 = Course("ENG 15", 2.0, id=next(id_gen))
catalog.append(eng15)

nano15 = Course("NANO 15", 4.0, id=next(id_gen))
catalog.append(nano15)
# CENG 15 is NANO 15

phys2a = Course("PHYS 2A", 4.0, id=next(id_gen))
phys2a.add_requisite(c1, pre) # or MATH 10A and B or MATH 20B or MATH 20C weird ass. I think it shoul dbe 20B
catalog.append(phys2a) 

phys4a = Course("PHYS 4A", 4.0, id=next(id_gen))
phys4a.add_requisite(c1, pre)
catalog.append(phys4a)

phys2b = Course("PHYS 2B", 4.0, id=next(id_gen))
phys2b.add_requisite(phys2a, pre) # or phy4a
phys2b.add_requisite(c2, pre) # or 20C
catalog.append(phys2b)

phys4b = Course("PHYS 4B", 4.0, id=next(id_gen))
phys4b.add_requisite(phys4a, pre)
phys4b.add_requisite(c2, pre)
catalog.append(phys4b)

chem6a = Course("CHEM 6A", 4.0, id=next(id_gen))
catalog.append(chem6a) # has a bunch of pre-college reqs >:(
# CHEM 6AH is exactly the same

chem6b = Course("CHEM 6B", 4.0, id=next(id_gen))
chem6b.add_requisite(chem6a, pre)
chem6b.add_requisite(c1, pre) # or math 10A apparently. 20b concurrent recommended
catalog.append(chem6b)
# CHEM 6BH is the same


bild2 = Course("BILD 2", 4.0, id=next(id_gen))
bild2.add_requisite(bild1, pre)
catalog.append(bild2)

bild3 = Course("BILD 3", 4.0, id=next(id_gen))
catalog.append(bild3)

bicd100 = Course("BICD 100", 4.0, id=next(id_gen))
bicd100.add_requisite(bild1, pre)
bicd100.add_requisite(bild3, pre)
catalog.append(bicd100)

bimm101 = Course("BIMM 101", 4.0, id=next(id_gen))
bimm101.add_requisite(bild1, pre)
catalog.append(bimm101)

bimm121 = Course("BIMM 121", 4.0, id=next(id_gen))
bimm121.add_requisite(bild1, pre)
catalog.append(bimm121)

cogs17 = Course("COGS 17", 4.0, id=next(id_gen))
catalog.append(cogs17)

cogs107a = Course("COGS 107A", 4.0, id=next(id_gen))
cogs107a.add_requisite(cogs17, pre) # or bild 12
catalog.append(cogs107a)

cogs107b = Course("COGS 107B", 4.0, id=next(id_gen))
cogs107b.add_requisite(cogs107a, pre)
catalog.append(cogs107b)

cogs115 = Course("COGS 115", 4.0, id=next(id_gen))
cogs115.add_requisite(cogs107a, pre) # or bild 10,12 or cogs 107b or cogs 17 (lol cogs 17 is pre for 107a)
catalog.append(cogs115)

esys101 = Course("ESYS 101", 4.0, id=next(id_gen))
esys101.add_requisite(bild1, pre)
catalog.append(esys101)

hds1 = Course("HDS 1", 4.0, id=next(id_gen))
catalog.append(hds1)

hds110 = Course("HDS 110", 4.0, id=next(id_gen))
hds110.add_requisite(hds1, pre)
catalog.append(hds110)

sio126 = Course("SIO 126", 4.0, id=next(id_gen))
sio126.add_requisite(bild1, pre)
catalog.append(sio126)

sio128 = Course("SIO 128", 4.0, id=next(id_gen))
sio128.add_requisite(bild1, pre) # bild 2 or bild 3
catalog.append(sio128)

econ1 = Course("ECON 1", 4.0, id=next(id_gen))
catalog.append(econ1)

# ECON 120A
econ120a = Course("ECON 120A", 4.0, id=next(id_gen))
econ120a.add_requisite(econ1, pre)
econ120a.add_requisite(c4, pre) # math 10C also works
catalog.append(econ120a)


# CSE 100
cse100 = Course("CSE 100", 4.0, id=next(id_gen))
cse100.add_requisite(cse21, pre)
cse100.add_requisite(cse29, pre) # put this in because curriculum requires 29 but if I didn't but 29 it could be 12/15L
catalog.append(cse100)

# CSE 101
cse101 = Course("CSE 101", 4.0, id=next(id_gen))
cse101.add_requisite(cse21, pre)
cse101.add_requisite(cse12, pre)
catalog.append(cse101)

# CSE 110
cse110 = Course("CSE 110", 4.0, id=next(id_gen))
cse110.add_requisite(cse100, pre)
catalog.append(cse110)

# CSE 120, 
cse120 = Course("CSE 120", 4.0, id=next(id_gen))
cse120.add_requisite(cse29, pre)
cse120.add_requisite(cse30, pre)
cse120.add_requisite(cse100, pre)
cse120.add_requisite(cse101, pre)
catalog.append(cse120)

# CSE 121, 
cse121 = Course("CSE 121", 4.0, id=next(id_gen))
cse121.add_requisite(cse120, pre)
catalog.append(cse121)

# CSE 122, 
cse122 = Course("CSE 122", 4.0, id=next(id_gen))
cse122.add_requisite(cse30, pre)
cse122.add_requisite(cse101, pre)
cse122.add_requisite(cse110, pre)
catalog.append(cse122)

# CSE 123, 
cse123 = Course("CSE 123", 4.0, id=next(id_gen))
cse123.add_requisite(cse29, pre)
cse123.add_requisite(cse101, pre)
cse123.add_requisite(cse110, pre)
catalog.append(cse123)

# CSE 124
cse124 = Course("CSE 124", 4.0, id=next(id_gen))
cse124.add_requisite(cse29, pre)
cse124.add_requisite(cse101, pre)
cse124.add_requisite(cse110, pre)
catalog.append(cse124)

# CSE 127, 
cse127 = Course("CSE 127", 4.0, id=next(id_gen))
cse127.add_requisite(cse21, pre)
cse127.add_requisite(cse120, pre)
catalog.append(cse127)

# CSE 132A, 
cse132a = Course("CSE 132A", 4.0, id=next(id_gen))
cse132a.add_requisite(cse100, pre)
catalog.append(cse132a)

# CSE 132C, 
cse132c = Course("CSE 132C", 4.0, id=next(id_gen))
cse132c.add_requisite(cse132a, pre)
catalog.append(cse132c)

# CSE 140, 
cse140 = Course("CSE 140", 4.0, id=next(id_gen))
cse140.add_requisite(cse20, pre)
cse140.add_requisite(cse30, pre)
catalog.append(cse140)

# CSE 140L, 
cse140l = Course("CSE 140L", 4.0, id=next(id_gen))
cse140l.add_requisite(cse20, pre)
cse140l.add_requisite(cse30, pre)
catalog.append(cse140l)

# CSE 141, 
cse141 = Course("CSE 141", 4.0, id=next(id_gen))
cse141.add_requisite(cse30, pre)
cse141.add_requisite(cse140, pre)
cse141.add_requisite(cse140l, pre)
catalog.append(cse141)

# CSE 141L, 
cse141l = Course("CSE 141L", 4.0, id=next(id_gen))
cse141l.add_requisite(cse30, pre)
cse141l.add_requisite(cse140, pre)
cse141l.add_requisite(cse140l, pre)
catalog.append(cse141l)

# CSE 142, 
cse142 = Course("CSE 142", 4.0, id=next(id_gen))
cse142.add_requisite(cse30, pre)
cse142.add_requisite(cse100, pre)
catalog.append(cse142)

# CSE 142L, 
cse142l = Course("CSE 142L", 4.0, id=next(id_gen))
cse142l.add_requisite(cse30, pre)
cse142l.add_requisite(cse100, pre)
catalog.append(cse142l)

# CSE 143, 
cse143 = Course("CSE 143", 4.0, id=next(id_gen))
cse143.add_requisite(cse140, pre)
catalog.append(cse143)

# CSE 145, 
cse145 = Course("CSE 145", 4.0, id=next(id_gen))
catalog.append(cse145)

# CSE 147,  
cse147 = Course("CSE 147", 4.0, id=next(id_gen))
cse147.add_requisite(cse30, pre)
catalog.append(cse147)

# CSE 148, 
cse148 = Course("CSE 148", 4.0, id=next(id_gen))
cse148.add_requisite(cse141, pre)
cse148.add_requisite(cse141l, pre)
catalog.append(cse148)

# CSE 160, 
cse160 = Course("CSE 160", 4.0, id=next(id_gen))
cse160.add_requisite(cse100, pre)
catalog.append(cse160)

dsc10 = Course("DSC 10", 4.0, id=next(id_gen))
catalog.append(dsc10)

dsc20 = Course("DSC 20", 4.0, id=next(id_gen))
dsc20.add_requisite(dsc10, pre)
catalog.append(dsc20)

dsc30 = Course("DSC 30", 4.0, id=next(id_gen))
dsc30.add_requisite(dsc20, pre)
catalog.append(dsc30)

dsc40a = Course("DSC 40A", 4.0, id=next(id_gen))
dsc40a.add_requisite(dsc10, pre)
dsc40a.add_requisite(c4, pre)
dsc40a.add_requisite(c3, pre)
catalog.append(dsc40a)

dsc40b = Course("DSC 40B", 4.0, id=next(id_gen))
dsc40b.add_requisite(dsc20, pre)
dsc40b.add_requisite(dsc40a, pre)
catalog.append(dsc40b)

dsc80 = Course("DSC 80", 4.0, id=next(id_gen))
dsc80.add_requisite(dsc30, pre)
dsc80.add_requisite(dsc40a, pre)
catalog.append(dsc80)

# DSC 100, 
dsc100 = Course("DSC 100", 4.0, id=next(id_gen))
dsc100.add_requisite(dsc40b, pre)
dsc100.add_requisite(dsc80, pre)
catalog.append(dsc100)
# NOTE it says it's restricted to ds25 majors only so i might just not include it

# DSC 102, 
dsc102 = Course("DSC 102", 4.0, id=next(id_gen))
dsc102.add_requisite(dsc100, pre)
catalog.append(dsc102)

# ECE 111, 
ece111 = Course("ECE 111", 4.0, id=next(id_gen))
ece111.add_requisite(cse140, pre)
catalog.append(ece111)

# ECE 140A, 
ece140a = Course("ECE 140A", 4.0, id=next(id_gen))
ece140a.add_requisite(cse8b, pre) # cse8b
catalog.append(ece140a)

# ECE 140B
ece140b = Course("ECE 140B", 4.0, id=next(id_gen))
ece140b.add_requisite(ece140a, pre)
catalog.append(ece140b)

# CSE 105, 
cse105 = Course("CSE 105", 4.0, id=next(id_gen))
cse105.add_requisite(cse12, pre)
cse105.add_requisite(cse20, pre)
cse105.add_requisite(cse21, pre)
catalog.append(cse105)

# CSE 106, 
cse106 = Course("CSE 106", 4.0, id=next(id_gen))
cse106.add_requisite(c3, pre)
cse106.add_requisite(c4, pre)
cse106.add_requisite(cse21, pre)
catalog.append(cse106)

# CSE 107, 
cse107 = Course("CSE 107", 4.0, id=next(id_gen))
cse107.add_requisite(cse21, pre)
cse107.add_requisite(cse101, pre)
cse107.add_requisite(cse105, pre)
catalog.append(cse107)

# CSE 130, 
cse130 = Course("CSE 130", 4.0, id=next(id_gen))
cse130.add_requisite(cse12, pre)
cse130.add_requisite(cse100, pre)
cse130.add_requisite(cse105, pre)
catalog.append(cse130)


# CSE 150A, 
cse150a = Course("CSE 150A", 4.0, id=next(id_gen))
cse150a.add_requisite(cse12, pre)
cse150a.add_requisite(cse29, pre)
cse150a.add_requisite(ece109, pre)
cse150a.add_requisite(c1, pre)
cse150a.add_requisite(c3, pre)
catalog.append(cse150a)

# DSC 120, 
dsc120 = Course("DSC 120", 4.0, id=next(id_gen))
dsc120.add_requisite(c3, pre)
dsc120.add_requisite(c4, pre)
dsc120.add_requisite(dsc80, pre)
catalog.append(dsc120)

# CSE 112, 
cse112 = Course("CSE 112", 4.0, id=next(id_gen))
cse112.add_requisite(cse110, pre)
catalog.append(cse112)

# CSE 118, 
cse118 = Course("CSE 118", 4.0, id=next(id_gen))
cse118.add_requisite(ece111, pre) # there's a whole bunch of other options here
catalog.append(cse118)

# CSE 125, 
cse125 = Course("CSE 125", 4.0, id=next(id_gen))
catalog.append(cse125)

# CSE 127, 
cse127 = Course("CSE 127", 4.0, id=next(id_gen))
cse127.add_requisite(cse21, pre)
cse127.add_requisite(cse120, pre)
catalog.append(cse127)

# CSE 131, 
cse131 = Course("CSE 131", 4.0, id=next(id_gen))
cse131.add_requisite(cse30, pre)
cse131.add_requisite(cse100, pre)
cse131.add_requisite(cse105, pre)
cse131.add_requisite(cse130, pre)
catalog.append(cse131)

# CSE 132B
cse132b = Course("CSE 132B", 4.0, id=next(id_gen))
cse132b.add_requisite(cse132a, pre)
catalog.append(cse132b)

# CSE 134B, 
cse134b = Course("CSE 134B", 4.0, id=next(id_gen))
cse134b.add_requisite(cse100, pre)
catalog.append(cse134b)

# CSE 135, 
cse135 = Course("CSE 135", 4.0, id=next(id_gen))
cse135.add_requisite(cse100, pre)
catalog.append(cse135)

# CSE 136, 
cse136 = Course("CSE 136", 4.0, id=next(id_gen))
cse136.add_requisite(cse135, pre)
catalog.append(cse136)

# CSE 150B
cse150b = Course("CSE 150B", 4.0, id=next(id_gen))
cse150b.add_requisite(cse12, pre)
cse150b.add_requisite(cse29, pre)
cse150b.add_requisite(ece109, pre)
cse150b.add_requisite(cse100, pre)
catalog.append(cse150b)

# CSE 151A
cse151a = Course("CSE 151A", 4.0, id=next(id_gen))
cse151a.add_requisite(cse12, pre)
cse151a.add_requisite(cse29, pre)
cse151a.add_requisite(ece109, pre)
cse151a.add_requisite(c3, pre)
cse151a.add_requisite(c4, pre)
catalog.append(cse151a)

# CSE 151B
cse151b = Course("CSE 151B", 4.0, id=next(id_gen))
cse151b.add_requisite(c4, pre)
cse151b.add_requisite(ece109, pre) # has a ton of other prereqs that are ORs
catalog.append(cse151b)

# CSE 152A, 
cse152a = Course("CSE 152A", 4.0, id=next(id_gen))
cse152a.add_requisite(c3, pre)
cse152a.add_requisite(cse12, pre)
cse152a.add_requisite(cse29, pre)
catalog.append(cse152a)

# CSE 152B, 
cse152b = Course("CSE 152B", 4.0, id=next(id_gen))
cse152b.add_requisite(cse152a, pre)
catalog.append(cse152b)

# CSE153 or CSE 153R
cse153 = Course("CSE 153", 4.0, id=next(id_gen)) # doesn't exist on the catalog :(
catalog.append(cse153)

# CSE 156, 
cse156 = Course("CSE 156", 4.0, id=next(id_gen))
cse156.add_requisite(cse12, pre)
cse156.add_requisite(cse29, pre)
cse156.add_requisite(ece109, pre)
catalog.append(cse156)

# CSE 158 or CSE 158R, 
cse158 = Course("CSE 158", 4.0, id=next(id_gen))
cse158.add_requisite(cse12, pre)
cse158.add_requisite(cse29, pre)
cse158.add_requisite(ece109, pre) # almost all the instances of ece 109 as a prereq are replaceable with cse 103
catalog.append(cse158)

# CSE 167 or CSE 167R, 
cse167 = Course("CSE 167", 4.0, id=next(id_gen))
cse167.add_requisite(cse100, pre)
catalog.append(cse167)

# CSE 163, 
cse163 = Course("CSE 163", 4.0, id=next(id_gen))
cse163.add_requisite(cse167, pre)
catalog.append(cse163)

# CSE 165, 
cse165 = Course("CSE 165", 4.0, id=next(id_gen))
cse165.add_requisite(cse167, pre)
catalog.append(cse165)

# CSE 166, 
cse166 = Course("CSE 166", 4.0, id=next(id_gen))
cse166.add_requisite(c3, pre)
cse166.add_requisite(cse100, pre)
catalog.append(cse166)


# CSE 168 or CSE 168R, 
cse168 = Course("CSE 168", 4.0, id=next(id_gen))
cse168.add_requisite(cse167, pre)
catalog.append(cse168)

# CSE 169, 
cse169 = Course("CSE 169", 4.0, id=next(id_gen))
cse169.add_requisite(cse167, pre)
catalog.append(cse169)

# CSE 170, 
cse170 = Course("CSE 170", 4.0, id=next(id_gen))
cse170.add_requisite(cse12, pre)
cse170.add_requisite(cogs10, pre) # cogs 1 also works
catalog.append(cse170)

# CSE 175,
cse175 = Course("CSE 175", 4.0, id=next(id_gen))
catalog.append(cse175)

#  CSE 176A, 
cse176a = Course("CSE 176A", 4.0, id=next(id_gen))
cse176a.add_requisite(cse110, pre)
catalog.append(cse176a)

# CSE 176E, 
cse176e = Course("CSE 176E", 4.0, id=next(id_gen))
catalog.append(cse176e)

# CSE 181, CSE 181R, 
cse181 = Course("CSE 181", 4.0, id=next(id_gen))
cse181.add_requisite(cse100, pre)
cse181.add_requisite(cse101, pre)
catalog.append(cse181)

# CSE 182, 
cse182 = Course("CSE 182", 4.0, id=next(id_gen))
cse182.add_requisite(cse100, pre)
catalog.append(cse182)

# CSE 184, 
cse184 = Course("CSE 184", 4.0, id=next(id_gen))
cse184.add_requisite(cse181, pre)
cse184.add_requisite(cse182, pre)
catalog.append(cse184)

bild4 = Course("BILD 4", 4.0, id=next(id_gen))
catalog.append(bild4)

# CSE 185, 
cse185 = Course("CSE 185" ,4.0, id=next(id_gen))
cse185.add_requisite(cse8b, pre)
cse185.add_requisite(cse12, pre)
cse185.add_requisite(c4, pre)
cse185.add_requisite(bild1, pre)
cse185.add_requisite(bild4, pre)
catalog.append(cse185)

# CSE 193, 
cse193 = Course("CSE 193", 4.0, id=next(id_gen))
catalog.append(cse193)

# CSE 194, 
cse194 = Course("CSE 194", 4.0, id=next(id_gen))
cse194.add_requisite(cse12, pre)
# or a bunch of other things, but they're all college related. basically anyone can take this
catalog.append(cse194)

cogs14a = Course("COGS 14A", 4.0, id=next(id_gen))
catalog.append(cogs14a)

cogs14b = Course("COGS 14B", 4.0, id=next(id_gen))
cogs14b.add_requisite(cogs14a, pre)
catalog.append(cogs14b)

# COGS 108, 
cogs108 = Course("COGS 108", 4.0, id=next(id_gen))
cogs108.add_requisite(cse8b, pre)
catalog.append(cogs108)

# COGS 109, 
cogs109 = Course("COGS 109", 4.0, id=next(id_gen))
cogs109.add_requisite(cogs14b, pre)
cogs109.add_requisite(c3, pre)
cogs109.add_requisite(cse8b, pre)
catalog.append(cogs109)

# COGS 118A, 
cogs118a = Course("COGS 118A", 4.0, id=next(id_gen))
cogs118a.add_requisite(cse8b, pre)
cogs118a.add_requisite(c3, pre)
cogs118a.add_requisite(c6, pre)
cogs118a.add_requisite(math180a, pre)
cogs118a.add_requisite(cogs108, pre) # tons of alternatives for this one
catalog.append(cogs118a)

# COGS 118B, 
cogs118b = Course("COGS 118B", 4.0, id=next(id_gen))
cogs118b.add_requisite(cse8b, pre)
cogs118b.add_requisite(c3, pre)
cogs118b.add_requisite(c6, pre)
cogs118b.add_requisite(ece109, pre)
cogs118b.add_requisite(cogs108, pre)
catalog.append(cogs118b)



# COGS 118C, 
cogs118c = Course("COGS 118C", 4.0, id=next(id_gen))
cogs118c.add_requisite(c3, pre)
cogs118c.add_requisite(cogs14b, pre)
cogs118c.add_requisite(cogs108, pre)
catalog.append(cogs118c)

# COGS 120, 
cogs120 = Course("COGS 120", 4.0, id=next(id_gen))
cogs120.add_requisite(cse12, pre)
cogs120.add_requisite(cogs10, pre) # alternatives here
catalog.append(cogs120)

# COGS 121, 
cogs121 = Course("COGS 121", 4.0, id=next(id_gen))
cogs121.add_requisite(cogs120, pre)
cogs121.add_requisite(cse8b, pre)
catalog.append(cogs121)

# COGS 122, 
cogs122 = Course("COGS 122", 4.0, id=next(id_gen))
cogs122.add_requisite(cogs120, pre)
catalog.append(cogs122)

# COGS 123, 
cogs123 = Course("COGS 123", 4.0, id=next(id_gen))
cogs123.add_requisite(cogs120, pre)
catalog.append(cogs123)

# COGS 124, 
cogs124 = Course("COGS 124", 4.0, id=next(id_gen))
cogs124.add_requisite(cogs121, pre)
catalog.append(cogs124)

# COGS 125, 
cogs125 = Course("COGS 125", 4.0, id=next(id_gen))
cogs125.add_requisites([cse8b, cogs120], [pre,pre])
catalog.append(cogs125)

# COGS 126, 
cogs126 = Course("COGS 126", 4.0, id=next(id_gen))
cogs126.add_requisite(cogs120, pre)
catalog.append(cogs126)

cogs1 = Course("COGS 1", 4.0, id=next(id_gen))
catalog.append(cogs1)

# COGS 127, 
cogs127 = Course("COGS 127", 4.0, id=next(id_gen))
cogs127.add_requisite(cse8b, pre)
cogs127.add_requisite(cogs1, pre)
catalog.append(cogs127)

# COGS 181, 
cogs181 = Course("COGS 181", 4.0, id=next(id_gen))
cogs181.add_requisite(cse8b, pre)
cogs181.add_requisite(c3, pre)
cogs181.add_requisite(c6, pre)
cogs181.add_requisite(math180a, pre)
cogs181.add_requisite(cogs118a, pre)
catalog.append(cogs181)

# COGS 185, 
cogs185 = Course("COGS 185", 4.0, id=next(id_gen))
cogs185.add_requisite(cogs118a, pre)
catalog.append(cogs185)

# COGS 186, 
cogs186 = Course("COGS 186", 4.0, id=next(id_gen))
cogs186.add_requisite(cogs108, pre)
catalog.append(cogs186)

# COGS 187A, 
cogs187a = Course("COGS 187A", 4.0, id=next(id_gen))
cogs187a.add_requisite(cse8b, pre)
cogs187a.add_requisite(cogs10, pre)
catalog.append(cogs187a)

# COGS 187B, 
cogs187b = Course("COGS 187B", 4.0, id=next(id_gen))
cogs187b.add_requisite(cogs187a, pre)
catalog.append(cogs187b)

# COGS 188, 
cogs188 = Course("COGS 188", 4.0, id=next(id_gen))
cogs188.add_requisite(cogs109, pre)
catalog.append(cogs188)

# COGS 189, 
cogs189 = Course("COGS 189", 4.0, id=next(id_gen))
cogs189.add_requisite(cogs108, pre)
catalog.append(cogs189)

# dsgn 1
dsgn1 = Course("DSGN 1", 4.0, id=next(id_gen))
catalog.append(dsgn1)

# DSGN 100, 
dsgn100 = Course("DSGN 100", 4.0, id=next(id_gen))
dsgn100.add_requisite(dsgn1, pre)
catalog.append(dsgn100)


econ100a = Course("ECON 100A", 4.0, id=next(id_gen))
econ100a.add_requisite(econ1, pre)
econ100a.add_requisite(c4, pre)
catalog.append(econ100a)

# ECON 172A, 
econ172a = Course("ECON 172A", 4.0, id=next(id_gen))
econ172a.add_requisite(econ100a, pre)
econ172a.add_requisite(ece109, pre) # or econ 120a
econ172a.add_requisite(c3, pre)
catalog.append(econ172a)

# ECON 172B, 
econ172b = Course("ECON 172B", 4.0, id=next(id_gen))
econ172b.add_requisite(econ172a, pre)
catalog.append(econ172b)

# ECE 140A, 
ece140a = Course("ECE 140A", 4.0, id=next(id_gen))
ece140a.add_requisite(cse8b, pre)
catalog.append(ece140a)

# ECE 140B, 
ece140b = Course("ECE 140B", 4.0, id=next(id_gen))
ece140b.add_requisite(ece140a, pre)
catalog.append(ece140b)

# ECE 148, 
ece148 = Course("ECE 148", 4.0, id=next(id_gen))
ece148.add_requisite(ece15, pre)
catalog.append(ece148)

# ENG 100D/ENG 100L, 
eng100d = Course("ENG 100D", 4.0, id=next(id_gen))
catalog.append(eng100d) # they're all college writing two, but I have no idea how to put that in properly

# EDS 124AR, 
eds124AR = Course("EDS 124AR", 4.0, id=next(id_gen))
catalog.append(eds124AR)

# EDS 124BR, 
eds124BR = Course("EDS 124BR", 4.0, id=next(id_gen))
catalog.append(eds124BR)

# LIGN 165, 
lign165 = Course("LIGN 165", 4.0, id=next(id_gen))
catalog.append(lign165)

# LIGN 167, 
lign167 = Course("LIGN 167", 4.0, id=next(id_gen))
lign167.add_requisite(c4, pre)
catalog.append(lign167)

# MUS 171, 
mus171 = Course("MUS 171", 4.0, id=next(id_gen))
catalog.append(mus171)

# MUS 172, 
mus172 = Course("MUS 172", 4.0, id=next(id_gen))
mus172.add_requisite(mus171, pre)
catalog.append(mus172)

# MUS 177, 
mus177 = Course("MUS 177", 4.0, id=next(id_gen))
mus177.add_requisite(mus172, pre)
catalog.append(mus177)


vis142 = Course("VIS 142", 4.0, id=next(id_gen))
catalog.append(vis142)
# VIS 141A, 
vis141a = Course("VIS 141A", 4.0, id=next(id_gen))
vis141a.add_requisite(vis142, pre)
catalog.append(vis141a)

# VIS 141B
vis141b = Course("VIS 141B", 4.0, id=next(id_gen))
vis141b.add_requisite(vis141a, pre)
catalog.append(vis141b)

# rest of the CSE catalog. apparently that's all the good stuff apart from the ones that are like research. Let's run it as is
open_electives = ["CSE 120", "CSE 121", "CSE 122", "CSE 123", "CSE 124", "CSE 127", "CSE 132C", "CSE 140", "CSE 140L", "CSE 141",
"CSE 141L", "CSE 142", "CSE 142L", "CSE 143", "CSE 145", "CSE 147", "CSE 148", "CSE 160"] + ["CSE 105", "CSE 106", "CSE 107","CSE 130", "CSE 132A", "CSE 140", "CSE 150A"] + ["CSE 112", "CSE 118", "CSE 125", "CSE 127", "CSE 131", "CSE 132B", "CSE 134B", "CSE 135", "CSE 136",
"CSE 140", "CSE 140L", "CSE 142", "CSE 142L", "CSE 145", "CSE 148", "CSE 150B", "CSE 151A", "CSE 151B",
"CSE 152A", "CSE 152B", "CSE 153", "CSE 156", "CSE 158", "CSE 163", "CSE 165", "CSE 166", 
"CSE 167", "CSE 168", "CSE 169", "CSE 170", "CSE 175", "CSE 176A", "CSE 176E", "CSE 181",
"CSE 182", "CSE 184", "CSE 185", "CSE 193", "CSE 194"]
############# Requirements ############
reqs = [
    # LDE 
    (1, ["CSE 3", "CSE 4GS", "CSE 6R", "CSE 8A", "CSE 42", "CSE 86", "CSE 90", 
         "CSE 91", "CSE 95", "CSE 99", "MAE 8", "COGS 9", "COGS 10", "COGS 18", 
         "ECE 15", "ENG 10", "ENG 15", "NANO 15"]), # CSE 180 somehow counts here
    (1, ["PHYS 4A", "PHYS 2A", "PHYS 2B", "PHYS 4B", "CHEM 6A", "CHEM 6B", "BILD 1", "BILD 2", "BILD 3", "BICD 100",
         "BIMM 101", "BIMM 121", "COGS 107A", "COGS 107B", "COGS 115", "ESYS 101", "HDS 110", "SIO 126", "SIO 128"]),
    (1, ["MATH 181A", "MATH 183", "ECON 120A", "ECE 109", "CSE 103"]),
    # systems elective
    (3, ["CSE 120", "CSE 121", "CSE 122", "CSE 123", "CSE 124", "CSE 127", "CSE 132C", "CSE 140", "CSE 140L", "CSE 141",
         "CSE 141L", "CSE 142", "CSE 142L", "CSE 143", "CSE 145", "CSE 147", "CSE 148", "CSE 160", "DSC 102",
         "ECE 111", "ECE 140A", "ECE 140B"]),
    # theory/ abstraction elective
    (3, ["CSE 105", "CSE 106", "CSE 107","CSE 130", "CSE 132A", "CSE 140", "CSE 150A", "DSC 120", "MATH 170A", "MATH 170B",
         "MATH 170C", "MATH 171A", "MATH 171B", "MATH 173A", "MATH 173B", "MATH 181D", "MATH 185", "MATH 187A"]),
    # applications of computing electives
    (3, ["CSE 112", "CSE 118", "CSE 125", "CSE 127", "CSE 131", "CSE 132B", "CSE 134B", "CSE 135", "CSE 136",
         "CSE 140", "CSE 140L", "CSE 142", "CSE 142L", "CSE 145", "CSE 148", "CSE 150B", "CSE 151A", "CSE 151B",
         "CSE 152A", "CSE 152B", "CSE 153", "CSE 156", "CSE 158", "CSE 163", "CSE 165", "CSE 166", 
         "CSE 167", "CSE 168", "CSE 169", "CSE 170", "CSE 175", "CSE 176A", "CSE 176E", "CSE 181",
         "CSE 182", "CSE 184", "CSE 185", "CSE 193", "CSE 194", "COGS 108", "COGS 109", "COGS 118A", "COGS 118B", "COGS 118C",
         "COGS 120", "COGS 121", "COGS 122", "COGS 123", "COGS 124", "COGS 125", "COGS 126", "COGS 127", "COGS 181",
         "COGS 185", "COGS 186", "COGS 187A", "COGS 187B", "COGS 188", "COGS 189", "DSC 100", "DSGN 100", 
         "ECON 172A", "ECON 172B", "ECE 140A", "ECE 140B", "ECE 148", "ENG 100D", "EDS 124AR", "EDS 124BR",
         "LIGN 165", "LIGN 167", "MATH 114", "MATH 155A", "MATH 189", "MUS 171", "MUS 172", "MUS 177", "VIS 141A", "VIS 141B"]),
    (6, open_electives)
]

template_dp = ca.read_csv("./files/CS26_dp.csv")
template = template_dp.curriculum if type(template_dp) == DegreePlan  else template_dp
template_catalog = Curriculum("Template", [])
for course in sorted(template.courses, key=lambda x:x.id):
    template_catalog = add_course(template_catalog, course.prefix + ' ' + course.num, catalog)
template_catalog.basic_metrics

results = []
(cs26_courses_min, cs26_curr_min) = cs.min_complexity(template_catalog, reqs, catalog)
(cs26_courses_max, cs26_curr_max) = cs.max_complexity(template_catalog, reqs, catalog)

#del cs26_curr_min.basic_metrics
cs26_curr_min.basic_metrics

#del cs26_curr_max.basic_metrics
cs26_curr_max.basic_metrics

print("##### INCLDUING DSC courses #####")
print("TEMPLATE: ")
print(template_catalog.metrics["complexity"], template_catalog.metrics["complexity"])
print("MAX: ")
print(cs26_courses_max, cs26_curr_max.metrics["complexity"], cs26_curr_max.metrics["complexity"])
ca.write_csv(cs26_curr_max, "./files/cs26_max.csv")
print("MIN: ")
print(cs26_courses_min, cs26_curr_min.metrics["complexity"], cs26_curr_min.metrics["complexity"])
results.append(
    {
    "section": "Including DSC courses",
    "results": {
        "template": {
            "url": urlize(dp_ize(template_catalog, template_dp), "", "CS26", 2025, "False"),
            "complexity": template_catalog.metrics['complexity'],
            "centrality": template_catalog.metrics['centrality']
        },
        "max": {
            "url": urlize(dp_ize(cs26_curr_max, template_dp), "", "CS26", 2025, "False"),
            "complexity": cs26_curr_max.metrics['complexity'],
            "centrality": cs26_curr_max.metrics['centrality']
        },
        "min": {
            "url": urlize(dp_ize(cs26_curr_min, template_dp), "", "CS26", 2025, "False"),
            "complexity": cs26_curr_min.metrics['complexity'],
            "centrality": cs26_curr_min.metrics['centrality']
        }
    }
})

# rest of the CSE catalog. apparently that's all the good stuff apart from the ones that are like research. Let's run it as is
open_electives = ["CSE 120", "CSE 121", "CSE 122", "CSE 123", "CSE 124", "CSE 127", "CSE 132C", "CSE 140", "CSE 140L", "CSE 141",
"CSE 141L", "CSE 142", "CSE 142L", "CSE 143", "CSE 145", "CSE 147", "CSE 148", "CSE 160"] + ["CSE 105", "CSE 106", "CSE 107","CSE 130", "CSE 132A", "CSE 140", "CSE 150A"] + ["CSE 112", "CSE 118", "CSE 125", "CSE 127", "CSE 131", "CSE 132B", "CSE 134B", "CSE 135", "CSE 136",
"CSE 140", "CSE 140L", "CSE 142", "CSE 142L", "CSE 145", "CSE 148", "CSE 150B", "CSE 151A", "CSE 151B",
"CSE 152A", "CSE 152B", "CSE 153", "CSE 156", "CSE 158", "CSE 163", "CSE 165", "CSE 166", 
"CSE 167", "CSE 168", "CSE 169", "CSE 170", "CSE 175", "CSE 176A", "CSE 176E", "CSE 181",
"CSE 182", "CSE 184", "CSE 185", "CSE 193", "CSE 194"]
############# Requirements ############
reqs = [
    # LDE 
    (1, ["CSE 3", "CSE 4GS", "CSE 6R", "CSE 8A", "CSE 42", "CSE 86", "CSE 90", 
         "CSE 91", "CSE 95", "CSE 99", "CSE 180", "MAE 8", "COGS 9", "COGS 10", "COGS 18", 
         "ECE 15", "ENG 10", "ENG 15", "NANO 15"]), # CSE 180 also counts
    (1, ["PHYS 4A", "PHYS 2A", "PHYS 2B", "PHYS 4B", "CHEM 6A", "CHEM 6B", "BILD 1", "BILD 2", "BILD 3", "BICD 100",
         "BIMM 101", "BIMM 121", "COGS 107A", "COGS 107B", "COGS 115", "ESYS 101", "HDS 110", "SIO 126", "SIO 128"]),
    (1, ["MATH 181A", "MATH 183", "ECON 120A", "ECE 109", "CSE 103"]),
    # systems elective
    (3, ["CSE 120", "CSE 121", "CSE 122", "CSE 123", "CSE 124", "CSE 127", "CSE 132C", "CSE 140", "CSE 140L", "CSE 141",
         "CSE 141L", "CSE 142", "CSE 142L", "CSE 143", "CSE 145", "CSE 147", "CSE 148", "CSE 160",
         "ECE 111", "ECE 140A", "ECE 140B"]),
    # theory/ abstraction elective
    (3, ["CSE 105", "CSE 106", "CSE 107","CSE 130", "CSE 132A", "CSE 140", "CSE 150A", "MATH 170A", "MATH 170B",
         "MATH 170C", "MATH 171A", "MATH 171B", "MATH 173A", "MATH 173B", "MATH 181D", "MATH 185", "MATH 187A"]),
    # applications of computing electives
    (3, ["CSE 112", "CSE 118", "CSE 125", "CSE 127", "CSE 131", "CSE 132B", "CSE 134B", "CSE 135", "CSE 136",
         "CSE 140", "CSE 140L", "CSE 142", "CSE 142L", "CSE 145", "CSE 148", "CSE 150B", "CSE 151A", "CSE 151B",
         "CSE 152A", "CSE 152B", "CSE 153", "CSE 156", "CSE 158", "CSE 163", "CSE 165", "CSE 166", 
         "CSE 167", "CSE 168", "CSE 169", "CSE 170", "CSE 175", "CSE 176A", "CSE 176E", "CSE 181",
         "CSE 182", "CSE 184", "CSE 185", "CSE 193", "CSE 194", "COGS 108", "COGS 109", "COGS 118A", "COGS 118B", "COGS 118C",
         "COGS 120", "COGS 121", "COGS 122", "COGS 123", "COGS 124", "COGS 125", "COGS 126", "COGS 127", "COGS 181",
         "COGS 185", "COGS 186", "COGS 187A", "COGS 187B", "COGS 188", "COGS 189", "DSGN 100", 
         "ECON 172A", "ECON 172B", "ECE 140A", "ECE 140B", "ECE 148", "ENG 100D", "EDS 124AR", "EDS 124BR",
         "LIGN 165", "LIGN 167", "MATH 114", "MATH 155A", "MATH 189", "MUS 171", "MUS 172", "MUS 177", "VIS 141A", "VIS 141B"]),
    (6, open_electives)
]

template = ca.read_csv("./files/CS26_dp.csv")
template = template_dp.curriculum if type(template_dp) == DegreePlan  else template_dp
template_catalog = Curriculum("Template", [])
for course in sorted(template.courses, key=lambda x:x.id):
    template_catalog = add_course(template_catalog, course.prefix + ' ' + course.num, catalog)
template_catalog.basic_metrics()

(cs26_courses_min, cs26_curr_min) = cs.min_complexity(template_catalog, reqs, catalog)
(cs26_courses_max, cs26_curr_max) = cs.max_complexity(template_catalog, reqs, catalog)

cs26_curr_min.basic_metrics()

cs26_curr_max.basic_metrics()
print("##### NOT INCLDUING DSC courses #####")
print("TEMPLATE: ")
print(template_catalog.metrics['complexity'], template_catalog.metrics["complexity"])
print("MAX: ")
print(cs26_courses_max, cs26_curr_max.metrics["complexity"], cs26_curr_max.metrics["centrality"])
ca.write_csv(cs26_curr_max, "./files/cs26_max_nodsc.csv")
print("MIN: ")
print(cs26_courses_min, cs26_curr_min.metrics["complexity"], cs26_curr_min.metrics["centrality"])
ca.write_csv(cs26_curr_max, "./files/cs26_min_nodsc.csv")

results.append(
    {
    "section": "Excluding DSC courses",
    "results": {
        "template": {
            "url": urlize(dp_ize(template_catalog, template_dp), "", "CS26", 2025, "False"),
            "complexity": template_catalog.metrics['complexity'],
            "centrality": template_catalog.metrics['centrality']
        },
        "max": {
            "url": urlize(dp_ize(cs26_curr_max, template_dp), "", "CS26", 2025, "False"),
            "complexity": cs26_curr_max.metrics['complexity'],
            "centrality": cs26_curr_max.metrics['centrality']
        },
        "min": {
            "url": urlize(dp_ize(cs26_curr_min, template_dp), "", "CS26", 2025, "False"),
            "complexity": cs26_curr_min.metrics['complexity'],
            "centrality": cs26_curr_min.metrics['centrality']
        }
    }
})

markdown_gen(results)
