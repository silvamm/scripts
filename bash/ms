#!/bin/bash

#######################################################################################
#  SETUP 
#######################################################################################

ROOT_PATH="/home/matheusmonteiro/Documents/Projetos"
CORE_NAME="shared-course-api"
ORCH_NAME="candidate-orchestrator-api"
IES_NAME="shared-institution-api"

CORE_PORT="8090"
ORCH_PORT="8094"
IES_PORT="8095"

COUNT=1
function printHeader(){
	echo
	echo  "- [$COUNT] $1 "
	echo
	((COUNT++))
}

#######################################################################################
#  STOP COMMANDS
#######################################################################################

function stopCore(){
	printHeader "Stop Core"

	fuser -k ${CORE_PORT}/tcp
    ps -ef | grep ${CORE_NAME} | grep java | head -1 | awk '{print $2}' | xargs -r kill

}

function stopOrch(){
	printHeader "Stop Orch"

	fuser -k ${ORCH_PORT}/tcp
	ps -ef | grep ${ORCH_NAME} | grep java | head -1 | awk '{print $2}' | xargs -r kill
}

function stopIes(){
	printHeader "Stop IES"

	fuser -k ${IES_PORT}/tcp
	ps -ef | grep ${IES_NAME} | grep java | head -1 | awk '{print $2}' | xargs -r kill
}

function stopGateway(){
	printHeader "Stop Gateway"

	fuser -k 8080/tcp
	docker ps --filter name=krakend* --filter status=running -aq | xargs -r docker stop
}
function stopDb(){
	printHeader "Stop DB"

	cd "${ROOT_PATH}/${CORE_NAME}"
	docker compose down
}

function stopAll(){
	stopDb
	stopCore
	stopOrch
	stopIes
	stopGateway
}

function stop(){
   arr=("$@")
   for ARG in "${arr[@]}"; do
      	case $ARG in
			c) stopCore;;
			db) stopDb;;
			a) stopAll;;  
	   		o) stopOrch;;  
	   		i) stopIes;;  
	   		g) stopGateway;;  
		esac
	done
}

#######################################################################################
#  RUN COMMANDS
#######################################################################################

function runDb(){
	printHeader "Run DB"

	cd "${ROOT_PATH}/${CORE_NAME}"
	docker compose up -d
}

function runCore(){
	printHeader "Run Core"

	cd "${ROOT_PATH}/${CORE_NAME}"
	gnome-terminal  --tab --title=${CORE_NAME} -- bash -c "mvn -DskipTests=true clean install; java -jar "${ROOT_PATH}/${CORE_NAME}/target/${CORE_NAME}-1.0-SNAPSHOT.jar" --server.port=${CORE_PORT} --institution.baseurl=http://localhost:${IES_PORT}" 
}

function runOrch(){
	printHeader "Run Orch"

	cd "${ROOT_PATH}/${ORCH_NAME}"
	gnome-terminal --tab --title=${ORCH_NAME} -- bash -c "mvn -DskipTests=true clean install; java -jar "${ROOT_PATH}/${ORCH_NAME}/target/${ORCH_NAME}-1.0-SNAPSHOT.jar" --server.port=${ORCH_PORT}" 
}

function runIes(){
	printHeader "Run IES"

	cd "${ROOT_PATH}/${IES_NAME}"
	gnome-terminal  --tab --title=${IES_NAME} -- bash -c "mvn -DskipTests=true clean install; java -jar "${ROOT_PATH}/${IES_NAME}/target/${IES_NAME}-1.0.0-SNAPSHOT.jar" --server.port=${IES_PORT}"
}

function runGateway(){
	printHeader "Run Gateway"

	cd "${ROOT_PATH}"
	cd "shared-gateway-api"
	gnome-terminal --tab --title=krakend -- bash -c "docker compose run -e FC_SETTINGS=config/settings/local -p 8080:8080 krakend"
}

function runAll(){
	runDb
	runCore
	runOrch
	runIes
	runGateway
}

function run(){
   arr=("$@")
   for ARG in "${arr[@]}"; do
      	case $ARG in
			c) runCore ;;
			db) runDb;;
			a) runAll;;  
	   		o) runOrch;;  
	   		i) runIes;;  
	   		g) runGateway;;  
		esac
	done
}

#######################################################################################
#  GIT COMMANDS
#######################################################################################

function gitCore(){
	cd "${ROOT_PATH}/${CORE_NAME}"
	git $1

}

function git(){
	arr=("$@")
	for ARG in "${arr[@]}"; do
		echo $ARG
	done
}


#######################################################################################
#  HELP 
#######################################################################################

function help(){
	echo
	echo "S Commands - For Stop"
	echo
	echo "-sa   Stop all"
	echo "-sc   Stop core"
	echo "-so   Stop orchestrator"
	echo "-sg   Stop gateway"
	echo "-si   Stop institutions"
	echo "-sdb  Stop database"
	echo
	echo "R Commands - For Run"
	echo
	echo "-ra   Run all"
	echo "-rc   Run core"
	echo "-ro   Run orchestrator"
	echo "-rg   Run gateway"
	echo "-ri   Run institutions"
	echo "-rdb  Run database"
	echo
}

#######################################################################################
#  MAIN 
#######################################################################################

set -f
IFS=, 
while getopts ":hr:s:g:" option; do
   case $option in
		h) 
			help
			exit;;
		r)  
            multi=($OPTARG)
			run "${multi[@]}"
			;;
		s)
            multi=($OPTARG)
			stop "${multi[@]}"
			;;
		g)
			multi=($OPTARG)
			git "${multi[@]}"
			;;		
		\?) 
			echo "Error: Invalid option"
			exit;;
   esac
done
exit 1

