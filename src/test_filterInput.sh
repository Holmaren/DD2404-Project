#!/bin/bash

#Testing different inputs to the noise filter

echo "### Test with empty stdin ###"
if  ./noiseFilter.py; then
	echo "Exit code of $?. Failure"
	exit
else
	echo "--- Succeded ---"
	
fi

echo "### Test with extra variable when calling the file ###"
if  ./noiseFilter.py ExtraVariable; then
	echo "Exit code of $?. Failure"
	exit
else
	echo "--- Succeded ---"
fi


echo "### Test with sequences of different length ###"

TESTINPUT=">test1"$'\n'"ABCD"$'\n'">test2"$'\n'"ABCDE"$'\n'

if  ./noiseFilter.py <<< "$TESTINPUT" ; then
	echo "Exit code of $?. Failure"
	exit
else
	echo "--- Succeded ---"
fi

echo "### Test with an empty string as input ###"

TESTINPUT2=""

if  ./noiseFilter.py <<< "$TESTINPUT2" ; then
	echo "Exit code of $?. Failure"
	exit
else
	echo "--- Succeded ---"
fi

echo "### Test with input that should succed ###"

TESTINPUT3=">test1"$'\n'"ABCDE"$'\n'">test2"$'\n'"ABCDE"$'\n'">test3"$'\n'"ABCDE"$'\n'

if ! ./noiseFilter.py <<< "$TESTINPUT3" ; then
	echo "Exit code of $?. Failure"
	exit
else
	echo "--- Succeded ---"
fi

echo "### Test what happens if all columns should be removed ###"

TESTINPUT4=">test1"$'\n'"ABCDE"$'\n'">test2"$'\n'"FGHIJ"$'\n'">test3"$'\n'"KLMNO"$'\n'

if ./noiseFilter.py <<< "$TESTINPUT4" ; then
	echo "Exit code of $?. Failure"
	exit
else
	echo "--- Succeded ---"
fi








