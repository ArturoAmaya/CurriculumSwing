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
If we're looking for best-case, order the courses lowest to highest impact. If we're looking for worst-case sort by highest to lowest.

#### Choose the courses to satisfy requirement counts
Here we need: a list of courses sorted by impact that also has what list each course can come from (called origins). Also need how many courses we need from each list (that's in $R$) Ex: 
- (4, ECE 165, ["TE 1", "TE 2", "TE 3"])
- (4, ECE 164, ["TE 1", "TE 3"])
- (5, ECE 166, ["TE 1", "TE 2", "TE 3"])
- (7, ECE 168, ["TE 1", "TE 2"])

or more generally:
- ($c_a$, $a$, [$o_a1$, $o_a2$,...])
- ($c_b$, $b$, [$o_b1$, $o_b2$,...])
- ($c_c$, $c$, [$o_c1$, $o_c2$,...])
- ($c_d$, $d$, [$o_d1$, $o_d2$,...])

##### Best case
For best case loop through top to bottom. For each course $x$ you look at:

- If it only has one origin and that origin still has classes remaining, add it to the corresponding list and -1 on that origin's remaining course count
- If it has more than one origin but all but one of those origins are full, add it to the list corresponding to the remaining origin and -1 on that origin's remaining course count
- If it has more than one non-full origin, look at those origin's remaining course count. If you choose $o_xi$ then the other non-full origins can be satisfied by the next {remaining course count} courses that have the same origin down the list. Hence we look at that impact, and choose the least bad one. Ex:

Given list:
- (2 A L1 L3)
- (2 B L2 L3 L5)
- (3 C L2 L4)
- (3 D L3)
- (3 E L4 L5)
- (3 F L2 L5)
- (4 G L1)
- (7 H L2)
- (8 I L3 L4)
- (8 J L3 L4 L5)



and requirements:
- L1: 1
- L2: 2
- L3: 3
- L4: 2
- L5: 1

To determine where A goes, we look at L1 and L3. L1 has only one required course so we look down the list for the next appearance of L1 (G, with a cost of 4). L3 has 3 required courses so we look down for the last of the next 3 courses with L3 in them (I with a cost of 8). So if A goes to L1 we incur an added cost of 8 in the best case. If A goes to L3 then we incur an added cost of 4. 8 is worse than 4 so A goes to L3. Then just decrease L3's remaining course count by one. 3-way options are similar except we add the two added costs. For example B can go to L2, L3 or L5 so we say if B goes to L2, L3 incurs +8 (I) and L5 incurs +3 (E or F). If B goes to L3, L2 incurs +3 (C), L5 incurs +3 (E or F). If L5 gets B, L2 incurs +3 (F), L3 incurs +8, (I). +8 vs +6 vs. +8. +6 is the best so we choose B->L3. In cases of true ties, remove everything up to the current choice and recursively call the same function with the current remaining course counts for each possible option. That way we reduce the number of recursive calls and overhead but we guarantee we get the smallest impact.

##### Worst Case
Do the same but choose based on worst impact. TODO add the fancy schmancy stuff that turns them into the same algorithm but just with reverse ordered lists.


#### Calculate impact
Now that you have the requirements satisfied and optimized, add those courses in to produce the curriculum you want to return. 

