#!/usr/bin/env python


import compare_trees as comp



'''
This file is used to test the function compareTrees in compare_trees.py
'''

#Use a random tree structure (in this case it's assymetric_0.5)
tree1="(sp2:131.37755,sp3:31.88776,(sp4:25.5102,(sp5:16.58163,(sp6:70.15306," + \
"(sp16:45.91837,(sp7:53.57143,(sp15:19.13265,(sp11:73.97959,(sp10:62.50000," + \
"(sp8:19.13265,(sp9:42.09184,(sp12:11.47959,(sp13:2.55102,(sp14:6.37755,"+ \
"sp1:24.23469):1.27551):6.37755):3.82653):2.55102):6.37755):16.58163):5.10204):8.92857):3.82653):7.65306):3.82653):1.27551):14.03061);"

#Create tree2 by doing 1 change in tree 1
tree2="(sp2:131.37755,sp3:31.88776,((sp5:16.58163,(sp6:70.15306," + \
"(sp16:45.91837,(sp7:53.57143,(sp15:19.13265,(sp11:73.97959,(sp10:62.50000," + \
"(sp8:19.13265,(sp9:42.09184,(sp12:11.47959,(sp13:2.55102,(sp14:6.37755,"+ \
"sp1:24.23469):1.27551):6.37755):3.82653):2.55102):6.37755):16.58163):5.10204):8.92857):3.82653):7.65306):3.82653):1.27551):14.03061);"


#A tree should be equal to itself, i.e. distance 0
assert (comp.compareTrees(tree1,tree1)==0)

#Tree2 should have one change from tree1, therefore distance 1
assert (comp.compareTrees(tree1,tree2)==1)

#Tree2 should be equal to itself
assert (comp.compareTrees(tree2,tree2)==0)

print "Test successful"

