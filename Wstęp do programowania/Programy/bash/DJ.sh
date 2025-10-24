#!/usr/bin/env bash

if [ $# -ne 3 ]; then
	echo "Poprawne użycie: ./DJ.sh DD MM RRRR"
else
	a=$((14-$2) // 12 )
	echo $a
fi
