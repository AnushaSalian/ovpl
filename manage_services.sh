#!/bin/bash

LOGGER='src/http_logging/http_logging_server.py'
ADAPTER='src/adapters/AdapterServer.py'
CONTROLLER='src/ControllerServer.py'

SERVICES=(LOGGER ADAPTER CONTROLLER)

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
    for arg in $args;
    do
    contains "$arg"
    if [ $status == 0 ]
    then    
      # Since the services ex. LOGGER are stored
      # inside input arguments, it is tricky to
      # extract a variable name from a variable. Refer
      # http://www.linuxquestions.org/questions/programming-9/bash-how-to-get-variable-name-from-variable-274718/ 
      # for more clearity.
      python ${!arg} &
      echo "$arg:$!" >> $PID_FILE
      sleep 1
    else
      echo 'Invalid arguments'
      usage
    fi
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
    for arg in $args;
    do
      if [ -f $PID_FILE ]
      then
        for process in `cat $PID_FILE`; 
        do
          process_name=`echo $process | cut -d ":" -f 1`
          process_id=`echo $process | cut -d ":" -f 2`
          if [[ $process_name == $arg ]]
          then
            kill $process_id;
            echo Stopping $arg 
            sed -i /$process_name/d $PID_FILE
            echo 'done'
          fi
        done
      else
        echo 'No services are running to be stopped'
      fi
    done
  fi
}

# To check if the service entered by the user
# is valid or not
contains() {
  echo $arg
  for service in $SERVICES;
  do
    if [ $arg == $service ]
    then
      status=0       
    else
      status=1
    fi
    return $status
  done
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

usage() {
  echo 'Usage:'
  echo 'Valid Services : LOGGER, ADAPTER and CONTROLLER'
  echo '1. For starting all the services:'
  echo ' a) ./manage_services.sh'
  echo ' b) ./manage_services.sh start'
  echo '2. For stopping all the services:'
  echo './manage_services.sh stop'
  echo '3. For an individual start or stop:'
  echo './manage_services.sh start SERVICE1'
  echo './manage_services.sh stop SERVICE1 SERVICE2'
}

if [ $# -eq '0' ]
then
  pre_check 
  stop_service 
  start_service

elif [ $1 == "-h" ]
then
  usage

# if arguments are greater than or equal to 1
# other than help	
else 
  input_args=($@)
  action=${input_args[0]}
  args=${input_args[@]:1}

  if [ "$action" == "start" ]
  then
    pre_check 
    stop_service "$args"
    start_service "$args"

  elif [ "$action" == "stop" ]
  then
    stop_service "$args"

  else
    echo 'Invalid action'
    usage
  fi
fi

