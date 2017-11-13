#!/bin/bash
group=$1
cd /Users/Rob/Desktop/Monocle-Fork/Monocle-Group$group

# Clear underlevel file if it exists

if [ -e underlevel.csv ]; then
    rm underlevel.csv
    echo "Old underlevel.csv was cleared."
else
    echo "No underlevel.csv file. Creating now."
fi

# Execute script to pull account stats
python3 scripts/my_export_accounts_csv.py

# Check if underlevel was produced, if not exit script
if [ ! -f underlevel.csv ]; then
    echo "No accounts in underlevel.csv"
    rm accounts*
    if [ -f invalid.csv ]; then
        rm invalid.csv
    fi
    exit 1
fi

# Obtain number of accounts that need to level up
new_count=$( wc -l underlevel.csv | awk {'print $1'} )
let new_count=new_count-1

# Revise config.py to the number of accounts that need to level up
current_grid=$(grep -e "GRID" monocle/config.py | awk -F "  #" '/1/ {print $1}')
sed -i '' -e "s@$current_grid@GRID = (1,$new_count)@" monocle/config.py

# Update account listing to the account credentials that need to level up
cp underlevel.csv ../TestAccounts/wash_team$group.csv

# Clean up
rm pickles/* accounts* 
if [ -f invalid.csv ]; then
    rm invalid.csv
fi

# Run scan
python3 scan-group$group.py > /Users/Rob/Desktop/Monocle-Fork/logs/scan-group$group.log 2>&1 &
