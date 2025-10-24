#!/usr/bin/env bash
echo "Hello $1 and $2!"

if [ "$1" == "Ala" ]; then
	echo "a gdzie jest Ola?"
elif [ "$1" == "Ola" ]; then
	echo "a gdzie się podziała Ala?"
else
	echo "gdzie się wszyscy podziali?"
fi
