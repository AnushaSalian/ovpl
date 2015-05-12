#!/bin/bash

LOGGER='src/http_logging/http_logging_server.py'
ADAPTER='src/adapters/AdapterServer.py'
CONTROLLER='src/ControllerServer.py'

SERVICES=("LOGGER" "ADAPTER" "CONTROLLER")

PID_FILE='/var/run/ads.pid'

# Start the services
start_service() {
  touch $PID_FILE
  if [ -z "$args" ]
  then
    python $LOGGER &
    #The variable "$!" has the PID of the last background process started. 
    echo "LOGGER:$!" >> $PID_FILE
    sleep 1
    python2 $ADAPTER &
    echo "ADAPTER:$!" >> $PID_FILE
    sleep 1
    python2 $CONTROLLER &
    echo "CONTROLLER:$!" >> $PID_FILE

  else
    for a in $args;
    do
      echo $a
      echo ${#SERVICES[@]}      
      for i in $SERVICES;
      do
	# This checks if service entered is valid.
        echo $i
        if [[ $i == $a ]] 
        then
          index=${SERVICES[$i]}
	  echo $index
	  case "$index" in
          '0')
            python $LOGGER &
            echo "LOGGER:$!" >> $PID_FILE
          ;;  
          
          '1')
            python2 $ADAPTER &
            echo "ADAPTER:$!" >> $PID_FILE
          ;;         
       
          '2')
            python2 $CONTROLLER &
            echo "CONTROLLER:$!" >> $PID_FILE
            ;;
          esac
        
        else
          continue 
        fi	
      done
    done 
  fi
}

# Stop the services 
stop_service() {
  if [ -z "$args" ]
  then
    if [ -f $PID_FILE ]
    then
      for i in `cat $PID_FILE`;
      do
        kill `echo $i | cut -d ":" -f 2`;
      done
      rm $PID_FILE
      echo 'done'
    else
      echo 'No services are running to be stopped'   
    fi

  else
    for a in $args;
    do
      if [ -f $PID_FILE ]
      then
        for i in `cat $PID_FILE`; 
        do
          process_name=`echo $i | cut -d ":" -f 1`
          process_id=`echo $i | cut -d ":" -f 2`
          if [[ $process_name == $a ]]
          then
            kill $process_id;
            echo Stopping $a 
            sed /$process_name/d $PID_FILE
            echo 'done'
          fi
        done
      else
        echo 'No services are running to be stopped'
      fi
    done
  fi
}

# Start mongod service
start_mongod() {
  service mongodb start
}

# Stop mongod service
stop_mongod() {
  service mongodb stop
}

# Repair mongod service
repair_mongod() {
  mongodb --repair
}

# Check if the service mongod is already running
pre_check() {
  service mongodb status
  if [ $? -ne 0 ]
  then
    echo 'service mongod is not running'
    stop_mongod
    echo 'stopping mongod'
    repair_mongod
    echo 'restarting mongod'
    start_mongod
    echo 'service mongod successfully restarted' 
  fi
}


if [ $# -eq '0' ]
then
  pre_check &&
  stop_service &&
  start_service
	
elif [ $# -eq '1' ]
then
  args=""
  case "$1" in
  'start')
    pre_check &&
    stop_service &&
    start_service 
    ;;
  
  'stop')
    echo 'stopping all the services...'
    stop_service
    ;;   

  *)
    echo 'Invalid action'
    ;;  
  esac
  
else
  input_args=($@)
  action=${input_args[0]}
  args=${input_args[@]:1}

  if [ "$action" == "start" ]
  then
    pre_check &&
   # stop_service - here also ??
    start_service "$args"

  elif [ "$action" == "stop" ]
  then
    stop_service "$args"

  else
    echo 'Incorrect usage of arguments'
  fi

fi

