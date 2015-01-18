#!/usr/bin/env python

import sys
import select
import dendropy

'''
What we want this script to do is to use dendropy to calculate the difference
between an inferred tree and the reference tree. This means that we need to input
two trees to be compared. To be able to pipe this script with the output of another (fnj)
, and also to follow the UNIX-philosophy, the inferred tree will be read from standard in 
while the reference tree will be read from a file where the filename is an input variable to the
script.
'''


def compareTrees(tree1Str,tree2Str):
	'''
	This is the function that uses dendropy to compare the
	two trees. 
	Input variables:
		- tree1Str: The first tree as a string
		- tree2Str: The second tree as a string
	'''

	#First we need to use dendropy to transform the two strings to tree objects
	tree1=dendropy.Tree.get_from_string(tree1Str, schema="newick")
	tree2=dendropy.Tree.get_from_string(tree2Str, schema="newick")

	#tree1.print_plot()
	#tree2.print_plot()
	
	#return tree1.euclidean_distance(tree2)
	return tree1.symmetric_difference(tree2)
	#return tree1.robinson_foulds_distance(tree2)


if __name__=="__main__":
	if len(sys.argv)!=2:
		sys.exit("Usage: ./compare_trees.py <referenceTreeFileName>")

	#If stdin is empty exit
	if sys.stdin.isatty():
		sys.exit("Error in compare_trees. No data in stdin")

	fileName=sys.argv[1]

	refTreeHandle=open(fileName)
	#Read the two trees as strings
	referenceTreeStr=refTreeHandle.read()
	inferredTreeStr=sys.stdin.read()

	#Call the function to compare the two trees using dendropy
	distance=compareTrees(referenceTreeStr,inferredTreeStr)

	#Print the calculated distance to stdout
	print distance
	


