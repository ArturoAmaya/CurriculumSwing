# Choosing Best/Worst-Case curricula

Problem: Currently, our notion of curriculum doesn't really understand electives. We just say things like "CSE / ECE TE 1" and call it a day. Since the prereqs of an elective can vary greatly, we don't assign any prereqs to the node "CSE  / ECE TE 1". However, when a student actually chooses a class from the list of approved ones, odds are it does have prereqs (i.e. added complexity). This means that our notion of curriculum complexity is an idealized lower bound. Things could be much worse.

This project attempts to find the best case and the worst case scenarios of actually filling out the electives of a curriculum. 

## The algorithm works in the following way:

### Take three inputs:
- $C$ the curriculum that we are analyzing. For the purposes of analysis, it has been stripped of all the embedded electives, so no "CSE / ECE TE 1" or 2, 3, 4, etc. Only required explicitly named courses.
- $R$, a list of requirements in the following format: $[(x_0, [c_w, c_q, ...]), (x_1, [c_f, c_g, ...]), ... , (x_i, [c_l, c_v, ...]), ...]$ where $[c_w, c_q, ...]$ represents a list of allowable courses for a given elective and $x_i$ indicates how many courses must be taken from that list.
- $A$, the catalog, or available courses

### Given those three inputs: 

#### Calculate add impact for all courses
Calculate the impact of adding each of the courses from a big set containing all the courses mentioned in $R$. The impact of adding course $c$ at the end of a sequence is defined as:

- +1 to blocking factor for every course $p \in c$'s entire prerequisite field. (They each help unblock one additional course)
- +$d_c$ for this course where $d_c$ is $c$'s delay factor. $d_c = \text{max}(d_i) + 1$ for $\forall d_i \in c$'s first-level prerequisite field. (i.e. this course was added at the end of a sequence. The longest sequence any of its direct prereqs was involved in is the longest sequence this course is involved in, but plus one because we added a course).
- +1 to delay factor $\forall x \in c$'s prereq field where $x$'s longest path ends in one of $c$'s level-one prereqs. TODO check this

Note that we claculate the impact of adding at the end of a sequence to avoid using any look-ahead type stuff which makes the worst case impact depend on stuff that may never make it in to the curriculum. In any case, something that is not at the end of a sequence has less impact than the course at the end of that sequence because adding the sequence-ender implies also adding the non sequence-ender. 

#### Sort by impact
If we're looking for best-case, order lowest to highest impact. If we're looking for worst-case sort by highest to lowest.

#### Choose the courses to satisfy requirement counts

