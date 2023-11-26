# Choosing Best/Worst-Case curricula

Problem: Currently, our notion of curriculum doesn't really understand electives. We just say things like "CSE / ECE TE 1" and call it a day. Since the prereqs of an elective can vary greatly, we don't assign any prereqs to the node "CSE  / ECE TE 1". However, when a student actually chooses a class from the list of approved ones, odds are it does have prereqs (i.e. added complexity). This means that our notion of curriculum complexity is an idealized lower bound. Things could be much worse.

This project attempts to find the best case and the worst case scenarios of actually filling out the electives of a curriculum. 