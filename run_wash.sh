#!/bin/bash
# To run execute: ./run_wash (group #) (time to run in seconds) (time to pause between restarts) (level to level up to)
# example: ./run_wash 5 600 60 1   This runs group 5, 600 seconds, pauses 60 seconds, levels to level 1

group=$1
run_time=$2
pause_time=$3
level=$4
run_time_minutes=$(($run_time/60))
running=1
counter=1
start_time=`date -u +%s`
log=/Users/Rob/Desktop/Monocle-Fork/logs/scan-group$group.log

countdown () {
seconds=$1
while [ $seconds -gt 0 ]; do
   echo -ne "Wait time: $seconds\033[0K\r"
   sleep 1
   : $((seconds--))
done
}

echo "Executing Group" $group "level up sequencing to level $level. Running each for" $run_time "seconds. Pause for" $pause_time "seconds."

cd /Users/Rob/Desktop/Monocle-Fork/Monocle-Group$group
cp scan.py scan-group$group.py

echo "Prepping for initial run. Checking if underlevel.csv file exists."
if [ -e underlevel.csv ]; then
    rm underlevel.csv
    echo "Old underlevel.csv was cleared."
else
    echo "No underlevel.csv file. Cleared to start."
fi

##### Initial run
echo "Starting initial scan. Will run for" $run_time "seconds (" $run_time_minutes "minutes )."
python3 -u scan-group$group.py > $log 2>&1 &

countdown $run_time

process_count=`ps -e | grep scan-group$group.py | wc -l`
echo "Checking process count:" $process_count

if [ $process_count -gt $running ]
then
    echo "Nicely stopping scan."
    kill -SIGINT $(ps -ef | grep -i scan-group$group.py | grep -v grep | awk '{print $2}')
fi

echo "Pausing" $pause_time "seconds to check if stopped nicely."
countdown $pause_time

process_count=`ps -e | grep scan-group$group.py | wc -l`
echo "Rechecking process count:" $process_count

if [ $process_count -gt $running ]
then
    echo "Hard stopping scan."
    kill -9 $(ps -ef | grep -i scan-group$group.py | grep -v grep | awk '{print $2}')
    sleep 2
    if [ -e monocle.sock ]
    then
        rm monocle.sock
    fi
else
    echo "Scan stopped nicely."
fi

echo "Initial run completed."

##### Level up runs
cd /Users/Rob/Desktop/Monocle-Fork/Monocle-Group$group
echo "Starting initial level up sequence for" $run_time "seconds (" $run_time_minutes "minutes )."
/Users/Rob/Desktop/Monocle-Fork/Monocle-Group$group/level_up_v2.sh $group $level > $log 2>&1 &

countdown $run_time

process_count=`ps -e | grep scan-group$group.py | wc -l`
echo "Checking process count:" $process_count

if [ $process_count -gt $running ]
then
    echo "Nicely stopping scan."
    kill -SIGINT $(ps -ef | grep -i scan-group$group.py | grep -v grep | awk '{print $2}')
fi

echo "Pausing" $pause_time "seconds to check if stopped nicely."
countdown $pause_time

process_count=`ps -e | grep scan-group$group.py | wc -l`
echo "Rechecking process count:" $process_count

if [ $process_count -gt $running ]
then
    echo "Hard stopping scan."
    kill -9 $(ps -ef | grep -i scan-group$group.py | grep -v grep | awk '{print $2}')
    sleep 2
    if [ -e monocle.sock ]
    then
        rm monocle.sock
    fi
else
    echo "Scan stopped nicely."
fi

# Check if underlevel was produced, if not exit script
if [ ! -f /Users/Rob/Desktop/Monocle-Fork/Monocle-Group$group/underlevel.csv ]; then
    echo "No underlevel.csv file available. Exiting completely."
    exit 1
fi

accounts_left_count=$( wc -l /Users/Rob/Desktop/Monocle-Fork/Monocle-Group$group/underlevel.csv | awk {'print $1'} )
(( accounts_left_count-- )) # Decrement to not count header line
echo "Checking accounts left to process to level $level:" $accounts_left_count

while [ $accounts_left_count -gt 0 ]; do
    echo "Starting looping level up sequence" $counter "for" $run_time "seconds (" $run_time_minutes "minutes )."
    /Users/Rob/Desktop/Monocle-Fork/Monocle-Group$group/level_up_v2.sh $group $level > $log 2>&1 &

    # If we are done early, bust out and clean up.
    if [ ! -e underlevel.csv ]
    then
        break
    fi

    countdown $run_time

    process_count=`ps -e | grep scan-group$group.py | wc -l`

    if [ $process_count -gt $running ]
    then
        echo "Nicely stopping scan."
        kill -SIGINT $(ps -ef | grep -i scan-group$group.py | grep -v grep | awk '{print $2}')
    fi

    echo "Pausing" $pause_time "seconds to check if stopped nicely."
    countdown $pause_time

    process_count=`ps -e | grep scan-group$group.py | wc -l`
    echo "Rechecking process count:" $process_count

    if [ $process_count -gt $running ]
    then
        echo "Hard stopping scan."
        kill -9 $(ps -ef | grep -i scan-group$group.py | grep -v grep | awk '{print $2}')
        sleep 2
        if [ -e monocle.sock ]
        then
            rm monocle.sock
        fi
    else
        echo "Scan stopped nicely."
    fi

    if [ -e /Users/Rob/Desktop/Monocle-Fork/Monocle-Group$group/underlevel.csv ]
    then
        accounts_left_count=$( wc -l /Users/Rob/Desktop/Monocle-Fork/Monocle-Group$group/underlevel.csv | awk {'print $1'} )
        (( accounts_left_count-- )) # Decrement to not count header line

        if [ $accounts_left_count -gt 0 ]
        then
            echo "Checking accounts left to process to level $level:" $accounts_left_count
        else
            echo "No more accounts to process. All leveled up."
        fi

        if [ $accounts_left_count -lt 11 ]
        then
            run_time=180
            run_time_minutes=$(($run_time/60))
        fi
    else
        echo "No more accounts to process. All leveled up."
    fi
    (( counter++ ))
done

# Clean up
if [ -e underlevel.csv ]; then
    rm underlevel.csv
    echo "Old underlevel.csv was cleared."
fi
rm /Users/Rob/Desktop/Monocle-Fork/logs/level_up-group$group.log

echo "Level up completed!"
end_time=`date -u +%s`
runtime=$((end_time-start_time))
minutes=$((runtime/60))

start=`date -r $start_time`
end=`date -r $end_time`

echo "Started:" $start
echo "Ended:" $end
echo "Run time of:" $runtime "seconds("$minutes"minutes)."




