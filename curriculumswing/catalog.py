import pandas as pd

# basic catalog generator. no notion of ORs
def make_catalog():
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
        if name == "MATH 20A":
            continue
        if name == "MATH 20B":
            courses[name].append("MATH 20A")
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
