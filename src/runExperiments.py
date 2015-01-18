#!/usr/bin/env python

'''
This file is used to run the experiments on all data and calculate
the statistics needed to create plots over the results. This is done by 
using subprocess to run commands and then read the outputs from the subprocesses.
OBS!!
This file uses relative paths which means it must be run from the directory "src"
and the datafiles have to be in the directory "../data" relative to the "src" directory
'''

import sys
import glob
import subprocess




def analyzeFiles(filePaths):
	'''
	This function will go through all files, call a subprocess and analyze them
	'''
	#Counting the nr of files tested
	totNrOfFiles=0
	

	for i in xrange(len(filePaths)):

		sumUnFiltered=0
		sumFiltered=0
		sumFilterDecrease=0
		sumFilterIncrease=0
		#Counting the nr of files in the current directory tested
		nrOfFiles=0

		curFilePath=filePaths[i]
		reference_trees=glob.glob(curFilePath[1])
		mutated_trees=glob.glob(curFilePath[0])

		reference_tree=reference_trees[0]

		for mutated_tree in mutated_trees:	

			nrOfFiles+=1

			unFilteredCall="cat " +	mutated_tree + " | ../bin/fastprot | ../bin/fnj -O newick | ./compare_trees.py " + reference_tree
			child=subprocess.Popen(unFilteredCall, stdout=subprocess.PIPE, shell=True)

			child.wait()
			curUnFilterAns=int(child.stdout.read())
			
			filteredCall="cat " +	mutated_tree + " | ./noiseFilter.py | ../bin/fastprot | ../bin/fnj -O newick | ./compare_trees.py " + reference_tree
			child=subprocess.Popen(filteredCall, stdout=subprocess.PIPE, shell=True)

			child.wait()
			curFilterAns=int(child.stdout.read())

			#Updating variables
			sumUnFiltered+=curUnFilterAns
			sumFiltered+=curFilterAns
			
			if (curUnFilterAns<curFilterAns):
				sumFilterIncrease+=1
			elif (curFilterAns<curUnFilterAns):
				sumFilterDecrease+=1

		totNrOfFiles+=nrOfFiles
		curMeanUnFiltered=float(sumUnFiltered)/float(nrOfFiles)
		curMeanFiltered=float(sumFiltered)/float(nrOfFiles)
		print "CurMeanUnFiltered",curMeanUnFiltered
		print "CurMeanFiltered",curMeanFiltered




#Some error checks, this file should not have any inputs

if(len(sys.argv)>1):
	sys.exit("runExperiments should not have any input variables")


#Defining a list of tuples were each tuple contains two strings,
#one to locate the mutated files and one to locate the reference tree
filePaths=[("../data/asymmetric_0.5/*.msl","../data/asymmetric_0.5/*.tree")]

#Count the amount of files to be able to compare later
childArgs=['find ../data/*/*.msl | wc -l']
child=subprocess.Popen(childArgs, stdout=subprocess.PIPE, shell=True)
child.wait()
nrFiles=int(child.stdout.read())

#print nrFiles

#IDEAS:
#Can use find */*.msl | wc -l to count the number of files and compare
#to the number of files processed here


#Start analyze of files

sys.stderr.write("Start processing files, please wait... \n")

analyzeFiles(filePaths)










