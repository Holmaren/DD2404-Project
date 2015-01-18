#!/bin/bash

#Testing the file compare_trees.py with different inputs

TREEFILE="../data/asymmetric_0.5/asymmetric_0.5.tree"

TREE="(sp2:131.37755,sp3:31.88776,(sp4:25.5102,(sp5:16.58163,(sp6:70.15306,
(sp16:45.91837,(sp7:53.57143))))));"

echo "### Test with empty stdin ###"
./compare_trees.py $TREEFILE;
OUT=$?

if  [ $OUT -eq 0 ] ; then
	echo "Exit code of $OUT. Failure"
	exit
else
	echo "--- Succeded ---"	
fi


echo "### Test without input variable ###"
./compare_trees.py;
OUT=$?

if [ $OUT -eq 0 ] ; then
	echo "Exit code of $OUT. Failure"
	exit
else
	echo "--- Succeded ---"	
fi


echo "### Test with inputs that should work ###"
./compare_trees.py $TREEFILE <<< "$TREE";
OUT=$?

if [ $OUT -ne 0 ] ; then
	echo "Exit code of $?. Failure"
	exit
else
	echo "--- Succeded ---"	
fi
