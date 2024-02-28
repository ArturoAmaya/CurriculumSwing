import pandas as pd
from curricularanalytics import Course

# basic catalog generator. no notion of ORs
def make_course_list():
    prereqs = pd.read_csv(("./files/prereqs.csv"))
    prereqs = prereqs[prereqs["Term Code"] == prereqs.iloc[-1]["Term Code"]]

    courses = dict()
    # course names
    unique_courses = prereqs['Course ID'].unique()
    for course in unique_courses:
        # filter down to the just the prereqs
        course_data = prereqs[prereqs['Course ID'] == course]

        subject_code = course_data.iloc[0]['Course Subject Code']
        number = course_data.iloc[0]['Course Number']

        subject_code = subject_code.strip()
        number = number.strip()

        name = subject_code + " " + number

        # override the MATh 20A and MATH 20B results
        courses[name] = []
        if name == "CSE 4GS":
            courses[name].append("MATH 20A")
            continue
        if name == "CSE 6GS":
            courses[name].append("MATH 20A")
            continue
        if name == "MATH 20A":
            continue
        if name == "MATH 20B":
            courses[name].append("MATH 20A")
            continue
        if name == "VIS 145B":
            courses[name].append("VIS 145A") # the first option, ICAM 102, DNE
            continue
        if name == "USP 191B":
            courses[name].append("USP 191A") # the first option, USP 190, DNE
            continue
        if name == "USP 185A":
            # USP 152 DNE anymore
            courses[name].append("USP 124")
            courses[name].append("USP 151")
            courses[name].append("USP 152A")
            courses[name].append("USP 153")
            continue
        if name == "USP 152B":
            courses[name].append("USP 152A")
            continue
        if name == "USP 177B":
            courses[name].append("USP 177A")
            continue
        if name == "TDMV 141":
            courses[name].append("TDMV 142") # TDMV 136 DNE
            continue
        if name == "TDHT 112":
            continue # the course DNE but it's in the database so I'll add it as no prereq
        if name == "TDHT 106":
            continue # the course DNE but it's in the database so I'll add it as no prereq
        if name == "TDDR 191":
            courses[name].append("TDPR 104")
            courses[name].append("TDDR 101")
            continue # the first req THPR 4 DNE
        if name == "SOCI 196B":
            courses[name].append("SOCI 196A") # misspelled as SOCE 
            continue
        if name == "SOCI 106M":
            courses[name].append("SOCI 60")
            courses[name].append("SOCI 178") # misspelled as SOCD
            continue
        if name == "SIO 162":
            courses[name].append("SIO 100") # ERTH 100 DNE
            continue
        if name == "SIO 102":
            courses[name].append("SIO 50") #ERTH 50 DNE
            courses[name].append("CHEM 6A")
            courses[name].append("CHEM 6B")
            courses[name].append("CHEM 6C")
            continue
        if name == "SIO 105":
            courses[name].append("SIO 50")
            continue
        if name == "SIO 129":
            continue # CHEM 140C DNE and SIO 129 hasn't been offered in two years
        # AMES 130A DNE:
        if name == "SE 110B":
            courses[name].append("SE 110A")
            continue
        if name == "SE 181":
            courses[name].append("SE 110A")
            continue
        if name == "SE 180":
            courses[name].append("SE 110A")
            courses[name].append("SE 130A") # AMES 132A DNE
            continue
        if name == "SE 110A":
            courses[name].append("SE 101A") # MAE 130A DNE
            courses[name].append("MATH 20D")
            continue
        if name == "SE 130A":
            courses[name].append("SE 110A") #MAE 131A DNE
            continue
        if name == "SE 171":
            courses[name].append("SE 110A") # MAE 131A and 131B DNE
            courses[name].append("SE 110B")
            continue
        if name == "SE 168":
            courses[name].append("SE 101C") # MAE 130C DNE
            courses[name].append("SE 131A")
            continue
        if name == "SE 101C":
            courses[name].append("SE 101B") # MAE 130B DNE
            courses[name].append("MATH 18") 
            continue
        if name == "SE 165":
            courses[name].append("SE 101C") # MAE 130C DNE
            continue
        if name == "SE 164":
            courses[name].append("SE 101C") # MAE 130C DNE
            courses[name].append("SE 110A")
            continue
        if name == "SE 131A":
            courses[name].append("MATH 20E")
            courses[name].append("SE 110B") # MAE 131B DNE
            courses[name].append("SE 3")
            continue
        if name == "SE 160A":
            courses[name].append("MAE 21")
            courses[name].append("MAE 30B")
            courses[name].append("SE 110A") # MAE 131A DNE
            continue
        if name == "SE 154":
            courses[name].append("SE 103")
            courses[name].append("SE 130A") # AMES 132A DNE
            continue
        if name == "SE 152":
            courses[name].append("SE 150A") # SE 150 DNE
            courses[name].append("SE 151A") 
            courses[name].append("SE 130B")
            continue
        if name == "SE 150B":
            courses[name].append("SE 150A") # SE 150 DNE 
            continue
        if name == "SE 142":
            courses[name].append("SE 110A")
            courses[name].append("SE 110B") # MAE 131A and B DNE
            continue
        if name == "SE 140A":
            courses[name].append("SE 130B")
            courses[name].append("SE 150A") # SE 150 DNE
            continue
        if name == "SE 132":
            courses[name].append("MAE 8")
            courses[name].append("SE 110A") # MAE 131A DNE it actually does tho
            courses[name].append("MAE 108")
            continue
        if name == "SE 102":
            courses[name].append("MAE 8")
            courses[name].append("SE 101A") # MAE 130A DNE
            continue
        if name == "RELI 197":
            continue # RELI 110A DNE
        if name == "MMW 12":
            continue # AWP DNE
        if name == "MCWP 40" or name == "MCWP 40R":
            continue # AWP 1 DNE
        if name == "MGT 121B":
            courses[name].append("MGT 121A") # MGT 111 DNE
            courses[name].append("MGT 181")
            continue
        if name == "MATH 187B":
            courses[name].append("MATH 187A") # MATH 187 DNE
            courses[name].append("MATH 18")
            continue
        if name == "MATH 174":
            courses[name].append("MATH 20D")
            courses[name].append("MATH 18") # MATH 20F DNE
            continue
        if name == "MATH 121A":
            courses[name].append("MATH 20C")
            courses[name].append("MATH 95") # EDS 30 DNE
            continue
        if name == "MAE 170":
            courses[name].append("PHYS 2C")
            courses[name].append("MAE 40") # MAE 140 DNE
            continue
        if name == "MAE 160":
            courses[name].append("MAE 20")
            courses[name].append("MAE 30A") # MAE 130A DNE
            courses[name].append("MAE 131A")
            continue
        if name == "MAE 131A":
            courses[name].append("MAE 30A") # MAE 130A DNE
            courses[name].append("MATH 20D")
            continue
        if name == "MAE 156A":
            courses[name].append("MAE 3")
            courses[name].append("MAE 131A")
            courses[name].append("MAE 170")
            courses[name].append("MAE 150")
            courses[name].append("MAE 30B") # MAE 130B DNE
            continue
        if name == "MAE 155A":
            courses[name].append("MAE 2")
            courses[name].append("MAE 21")
            courses[name].append("MAE 104")
            courses[name].append("MAE 30B") # MAE 130C DNE
            courses[name].append("SE 160A") # MAE 130B DNE
            continue
        if name == "MAE 132":
            courses[name].append("SE 101B") #MAE 130B DNE
            continue
        if name == "MAE 130":
            courses[name].append("MATH 18")
            courses[name].append("MAE 30B")
            continue
        if name == "LTWR 101":
            courses[name].append("LTWR 8A")
            # the other option DNE LTSP 50A,B,C
            continue
        if name == "LTEA 151":
            continue # option LIHL 132 doesn't show on online catalog
        if name == "JWSP 3":
            courses[name].append("JWSP 2")
            continue
        if name == "JWSP 2":
            courses[name].append("JWSP 1")
            continue
        if name == "JWSP 101":
            courses[name].append("JWSP 3")
            continue
        if name == "JWSP 102":
            courses[name].append("JWSP 101")
            continue
        if name == "JWSP 103":
            courses[name].append("JWSP 102")
            continue
        if name == "HINE 161":
            del courses[name] # course DNE afaik
            continue
        if name == "HINE 153B":
            continue # HINE 135A DNE
        if name == "HDS 191":
            courses[name].append("HDS 1")
            courses[name].append("HDS 181")
            continue
        if name == "HDS 181":
            courses[name].append("HDS 1")
            courses[name].append("BIEB 100")
            continue
        if name == "HDS 110" or name == "HDS 120" or name == "HDS 122" or name == "HDS 133":
            courses[name].append("HDS 1")
            continue
        if name == "HDS 150":
            courses[name].append("HDS 181")
            continue
        if name == "FMPH 194":
            courses[name].append("FMPH 40")
            courses[name].append("FMPH 50")
            courses[name].append("FMPH 101")
            courses[name].append("FMPH 102")
            courses[name].append("FMPH 110")
            courses[name].append("FMPH 120")
            courses[name].append("FMPH 193")
            continue
        if name == "FMPH 193":
            courses[name].append("FMPH 40")
            courses[name].append("FMPH 50")
            courses[name].append("FMPH 101")
            courses[name].append("FMPH 102")
            courses[name].append("FMPH 110")
            continue
        if name == "ETHN 191B":
            courses[name].append("ETHN 191A")
            continue
        if name == "ETHN 191A":
            continue # apparently ETHN 100 DNE and neither does the 191 series
        if name == "ERC 92":
            continue # no prereqs, invitation
        if name == "EDS 120":
            courses[name].append("DOC 1")
            continue
        if name == "ECON 122":
            courses[name].append("ECON 120B")
            courses[name].append("MATH 18")
            continue
        if name == "ECE 187":
            courses[name].append("MATH 20A")
            courses[name].append("MATH 20B")
            courses[name].append("MATH 20C")
            courses[name].append("MATH 20D")
            courses[name].append("PHYS 2A")
            courses[name].append("PHYS 2B")
            courses[name].append("PHYS 2C")
            courses[name].append("PHYS 2D")
            courses[name].append("ECE 101")
            courses[name].append("MATH 18")
            continue
        if name == "ECE 175B":
            courses[name].append("ECE 175A")
            continue
        if name == "ECE 161B":
            courses[name].append("ECE 161A")
            continue
        if name == "ECE 159B":
            courses[name].append("ECE 159") # unsure about this one
            continue
        if name == "COMM 114C":
            courses[name].append("COMM 10")
            continue
        if name == "COMM 102M" or name == "COMM 102P" or name == "COMM 102T":
            courses[name].append("COMM 10")
            courses[name].append("COMM 101")
            continue
        if name == "CHEM 40CH":
            courses[name].append("CHEM 40BH")
            continue
        if name == "CHEM 40C":
            courses[name].append("CHEM 40B")
            continue
        if name == "CHEM 40BH":
            courses[name].append("CHEM 40AH")
            continue
        if name == "CHEM 40B":
            courses[name].append("CHEM 40A")
            continue
        if name == "CHEM 186":
            courses[name].append("MATH 20C")
            courses[name].append("CHEM 126B")
            continue
        if name == "CHEM 185":
            courses[name].append("MATH 20C")
            courses[name].append("CHEM 126B")
            continue
        if name == "CHEM 145":
            courses[name].append("CHEM 40B")
            continue
        if name == "CHEM 145":
            courses[name].append("CHEM 40B")
            courses[name].append("CHEM 143B")
            continue
        if name == "CHEM 143D":
            courses[name].append("CHEM 40C")
            courses[name].append("CHEM 143B")
            continue
        if name == "CHEM 143C":
            courses[name].append("CHEM 43A")
            courses[name].append("CHEM 40B")
            continue
        if name == "CHEM 142":
            courses[name].append("CHEM 40B")
            courses[name].append("BIBC 100")
            continue
        if name == "CHEM 141":
            courses[name].append("CHEM 40A")
            continue
        if name == "CHEM 135":
            courses[name].append("CHEM 130")
            courses[name].append("MATH 20D")
            continue
        if name == "CHEM 123":
            courses[name].append("CHEM 120A")
            courses[name].append("CHEM 43A")
            courses[name].append("CHEM 120B")
            continue
        if name == "CHEM 120A":
            courses[name].append("CHEM 6C")
            courses[name].append("CHEM 40A")
            continue
        if name == "CHEM 116":
            courses[name].append("CHEM 40C")
            courses[name].append("CHEM 114A")
            continue
        if name == "CHEM 113":
            courses[name].append("CHEM 40C")
            continue
        if name == "CHEM 109":
            courses[name].append("CHEM 43A")
            courses[name].append("CHEM 114A")
            continue
        if name == "CHEM 108":
            courses[name].append("CHEM 43A")
            courses[name].append("CHEM 114A")
            continue
        if name == "CHEM 105A":
            courses[name].append("CHEM 100A")
            courses[name].append("PHYS 2BL")
            courses[name].append("CHEM 126A")
            continue
        if name == "CHEM 100A":
            courses[name].append("CHEM 6C")
            courses[name].append("CHEM 7L")
            continue
        if name == "CGS 100B":
            courses[name].append("CGS 100A")
            continue
        # get the number of prereq IDs
        prereq_count = course_data['Prereq Sequence ID'].unique()
        for count in prereq_count:
            equivalent_preqs = course_data[course_data['Prereq Sequence ID'] == count]
            try:
                chosen_preq = equivalent_preqs.iloc[0]
                courses[name].append(chosen_preq["Prereq Subject Code"].strip() + " " + chosen_preq["Prereq Course Number"].strip())
            except:
                continue
    return courses

def course_find(name: str, li: list[Course])->Course:
    for course in li:
        if course.name == name:
            return course
        
def make_catalog(course_list: dict[list[str]])->list[Course]:
    catalog = []
    # while the list isn't empty try to add courses
    while course_list:
        for course in list(course_list.keys()):
            try: 
                c = Course(course, 4.0) # for NOW
                for preq in course_list[course]:
                    c.add_requisite(course_find(preq, catalog), "pre")
                catalog.append(c)
                # remove from course_list if we successfully added to catalog
                del course_list[course]
            except: 
                # if we have an error, it's probably that the prereq isn't in there yet. Just continue and add it next loop
                continue
    return catalog