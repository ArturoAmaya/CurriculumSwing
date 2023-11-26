# Choosing Best/Worst-Case curricula

Problem: Currently, our notion of curriculum doesn't really understand electives. We just say things like "CSE / ECE TE 1" and call it a day. Since the prereqs of an elective can vary greatly, we don't assign any prereqs to the node "CSE  / ECE TE 1". However, when a student actually chooses a class from the list of approved ones, odds are it does have prereqs (i.e. added complexity). This means that our notion of curriculum complexity is an idealized lower bound. Things could be much worse.

This project attempts to find the best case and the worst case scenarios of actually filling out the electives of a curriculum. 

## The algorithm works in the following way:

### Take three inputs:
- $C$ the curriculum that we are analyzing. For the purposes of analysis, it has been stripped of all the embedded electives, so no "CSE / ECE TE 1" or 2, 3, 4, etc. Only required explicitly named courses.
- $R$, a list of requirements in the following format: $[(x_0, [c_w, c_q, ...]), (x_1, [c_f, c_g, ...]), ... , (x_i, [c_l, c_v, ...]), ...]$ where $[c_w, c_q, ...]$ represents a list of allowable courses for a given elective and $x_i$ indicates how many courses must be taken from that list.
- $A$, the catalog, or available courses

### Given those three inputs: 

Calculate the impact of adding 

