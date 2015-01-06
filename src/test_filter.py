#!/usr/bin/env python

import noiseFilter as filt
from Bio.Seq import Seq
import test

#Used to test the functions isNoisy and removeColumns in noiseFilter.py

#Test isNoisy

#This should be noisy
test1=['X','-','-','-','-']
assert filt.isNoisy(test1)

#This should also be noisy
test2=['X','A','B','C','D']
assert filt.isNoisy(test2)

#This too
test3=['X','X','A','A','B']
assert filt.isNoisy(test3)

#But this should not be noisy
test4=['X','X','X','A','B','X']
assert not filt.isNoisy(test4)


#Testing removeColumns

sequences=[Seq('AMK-Q-A-I-LL--T'),Seq('A-K-QAA-IMML--T')]

removeCols=[0,4,3,6]

sequencesAfter=[Seq('MK--I-LL--T'),Seq('-KA-IMML--T')]

resultSeq=filt.removeColumns(sequences,removeCols)

for i in xrange(len(sequences)):
	assert str(sequencesAfter[i])==str(resultSeq[i])

#print "supposeToBe",sequencesAfter
#print "is",resultSeq




