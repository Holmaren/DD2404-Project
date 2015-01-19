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
	This function will go through all files, call a subprocess and analyze them.
	Input variables:
		-filePaths: a list of file paths for the data

	Returns:
		-totNrOfFiles: a integer to count how many files have been processed
		-listMeans: A list with tuples, one for each referece tree. The first position of the 
					tuples contain the mean for the difference between trees that have 
					been through the noise filter and the reference tree and the second position
					contains the difference between the mutated trees and the reference trees 
					without having been through the noise filter.
		-listChanges: A list with tuples, one tuple per reference tree. The first position of the
						tuples contain the number of trees where the difference decreased after
						being through the noise filter and the second position the number of trees
						where the difference increased. 
	'''
	#Counting the nr of files tested
	totNrOfFiles=0
	
	#Lists to save the results from every 
	listMeans=[]
	listChanges=[]

	nrFilePaths=len(filePaths)

	for i in xrange(nrFilePaths):


		sys.stderr.write("--- Processing file path "+str(i+1)+" of "+str(nrFilePaths)+" --- \n"	)


		sumUnFiltered=0
		sumFiltered=0
		#Variables to count in how many cases the noisefilter decreased/increased the difference
		sumFilterDecrease=0
		sumFilterIncrease=0
		#Counting the nr of files in the current directory tested
		nrOfFiles=0

		curFilePath=filePaths[i]
		reference_trees=glob.glob(curFilePath[1])
		mutated_trees=glob.glob(curFilePath[0])

		#There should only be once reference tree in every file path
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
			
			#Checking if using the filter increased or decreased the difference to the reference tree
			if (curUnFilterAns<curFilterAns):
				sumFilterIncrease+=1
			elif (curFilterAns<curUnFilterAns):
				sumFilterDecrease+=1

		totNrOfFiles+=nrOfFiles
		curMeanUnFiltered=float(sumUnFiltered)/float(nrOfFiles)
		curMeanFiltered=float(sumFiltered)/float(nrOfFiles)
		#print "CurMeanUnFiltered",curMeanUnFiltered
		#print "CurMeanFiltered",curMeanFiltered

		#Save all results
		listMeans.append((curMeanFiltered,curMeanUnFiltered))
		listChanges.append((sumFilterDecrease,sumFilterIncrease))


	return (totNrOfFiles,listMeans,listChanges)


#Some error checks, this file should not have any inputs

if(len(sys.argv)>1):
	sys.exit("runExperiments should not have any input variables")


#Defining a list of tuples were each tuple contains two strings,
#one to locate the mutated files and one to locate the reference tree
filePaths=[("../data/asymmetric_0.5/*.msl","../data/asymmetric_0.5/*.tree")]

#Count the amount of files to be able to compare later
childArgs=['find ../data/asymmetric_0.5/*.msl | wc -l']
child=subprocess.Popen(childArgs, stdout=subprocess.PIPE, shell=True)
child.wait()
nrFiles=int(child.stdout.read())
if(nrFiles==0):
	sys.exit('No test files found. Be sure to run the file from the correct directory')

#print nrFiles

#IDEAS:
#Can use find */*.msl | wc -l to count the number of files and compare
#to the number of files processed here


#Start analyze of files

sys.stderr.write("Start processing files, please wait... \n")

(totFiles,listMeans,listChanges)=analyzeFiles(filePaths)

if(totFiles!=nrFiles):
	sys.stderr.write("WARNING: "+str(nrFiles)+" files ending with .msl were found in the "+\
	"specified directory but only "+str(totFiles)+" files has been analyzed \n")


#Printing data to standard out
directoryNames=["asymmetric_0.5","asymmetric_1.0","asymmetric_2.0","symmetric_0.5","symmetric_1.0","symmetric_2.0"]

print "Directory Name 	Mean Filtered	Mean UnFiltered		Decreased	Increased"

for i in xrange(len(listMeans)):
	(meanFiltered,meanUnFiltered)=listMeans[i]
	(filterDecreased,filterIncreased)=listChanges[i]

	print directoryNames[i], "	",meanFiltered,"		",meanUnFiltered,"		"\
	,filterDecreased,"		",filterIncreased


	
	










