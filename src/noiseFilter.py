#!/usr/bin/env python

import sys
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import select


def isNoisy(column):
	'''
	Function that checks if a column i noisy and returns true if it is. A column is
	considered noisy if:
	- There are more than 50% indels
	- At least 50% of amino acids are unique
	- No amino acid appears more than twice

	Input variables:
		column is a list of amino acids and represents one column in a multialignment
	'''

	#The length of the column
	colLength=len(column)

	#First we check for indels, these are represented by a hyphen (-)
	nrIndels=column.count('-')
	
	if float(nrIndels)/float(colLength)>0.5:
		return True

	#Next we check for the unique amino acids
	#If we make the list into a set we only get unique objects
	uniqueSet=set(column)
	if float(len(uniqueSet))/float(colLength)>0.5:
		return True

	#Last we check if no amino acid appears more than twice
	#Make a list of the occurences of each amino acid
	occ=[column.count(acid) for acid in uniqueSet]

	if max(occ)<=2:
		return True

	return False
	

def removeColumns(sequences,listOfColNum):
	'''
	Function to remove all columns specified in listOfColNum
	from the sequence alignment.
	
	Input Variables:
		sequences - A list of the sequences in the alignment
		listOfColNum - A list of numbers specifying which columns to remove
	'''

	#We have to keep track of the nr of columns removed since this will shift which columns are to
	#be removed later
	nrColsRemoved=0

	#Sort the list
	listOfColNum.sort()
	
	for colNum in listOfColNum:
		removeCol=colNum-nrColsRemoved
		for i in xrange(len(sequences)):
			sequence=sequences[i]
			newSequence=sequence[0:removeCol]+sequence[removeCol+1:]
			#print newSequence
			sequences[i]=newSequence
		nrColsRemoved+=1

	return sequences





#The filter will read the sequences from standard in, therefore there should be only 1 argument in argv
if __name__=="__main__":
	if len(sys.argv)>1:
		sys.exit("Usage: noiseFilter.py. The program reads the sequences from standard in")

	#If stdin is empty exit
	if not select.select([sys.stdin,],[],[],0.0)[0]:
		sys.exit("No data in stdin")

	#Lists to save the record IDs, Sequences, name and descriptions
	recordIds=[]
	recordSeqs=[]
	recordNames=[]
	recordDesc=[]
	#All the sequences should have the same length, if they don't there is some error
	seqLength=-1

	for record in SeqIO.parse(sys.stdin,"fasta"):
		if seqLength==-1:
			seqLength=len(record.seq)
			#print record.seq
			#print record.id
		else:
			#print len(record.seq)
			#print seqLength
			#sys.stderr.write(str(len(record.seq))+"\n")
			#sys.stderr.write(str(seqLength)+"\n")
			if seqLength!=len(record.seq):
				sys.exit("Not all sequences have the same length")

		recordIds.append(record.id)
		recordSeqs.append(record.seq)
		recordNames.append(record.name)
		recordDesc.append(record.description)
		#print record.id
		#print record.seq

	#If there were no sequences read on stdin we exit
	if len(recordIds)==0:
		sys.exit("No sequences have been read")


	#Iterate through all columns and check if they are noisy
	noisyColumns=[]
	for i in xrange(seqLength):
		curColumn=[recordSeqs[a][i] for a in xrange(len(recordSeqs))]
		if isNoisy(curColumn):
			noisyColumns.append(i)

	#If the nr of columns to be removed is the same as the length of the sequences all columns are removed
	nrOfRemovedCols=len(noisyColumns)
	if nrOfRemovedCols==seqLength:
		sys.exit("All columns were removed")

	recordSeqs=removeColumns(recordSeqs,noisyColumns)

	#sys.stderr.write(str(nrOfRemovedCols)+" columns were removed\n")

	#Now we write the alignment to stdout
	seqRecords=[]
	for i in xrange(len(recordSeqs)):
		newRecord=SeqRecord(recordSeqs[i],id=recordIds[i],name=recordNames[i],description=recordDesc[i])
		seqRecords.append(newRecord)

	SeqIO.write(seqRecords,sys.stdout,"fasta")










