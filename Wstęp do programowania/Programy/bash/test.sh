#!/usr/bin/env bash

#!/usr/bin/env bash

x=$(ls $1 -al | wc -l)
x=$(($x-1))

echo "W tym folderze znajduje się $x elementów."