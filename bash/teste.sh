#!/bin/bash

#######################################################################################
#  SETUP 
#######################################################################################

FOLDER_PROJECTS_PATH="/home/matheusmonteiro/Documents/Projetos"

declare -A NAME_OF=(["c"]="shared-course-api" ["o"]="candidate-orchestrator-api" ["i"]="shared-institution-api")
declare -A PORT_OF=(["c"]="8090" ["o"]="8094" ["i"]="9095")
declare -A ARGS_FOR_JAVA_OF=(["c"]="--institution.baseurl=http://localhost:"${PORT_OF[i]}"")

#######################################################################################
#  STOP COMMANDS
#######################################################################################

function stop(){
    echo "Stop "${NAME_OF[$1]}""
    fuser -k "${PORT_OF[$1]}"/tcp
    ps -ef | grep "${NAME_OF[$1]}" | grep java | head -1 | awk '{print $2}' | xargs -r kill
}

function stopGateway(){
	echo "Stop Gateway"

	fuser -k 8080/tcp
	docker ps --filter name=krakend* --filter status=running -aq | xargs -r docker stop
}
function stopDb(){
	echo "Stop DB"

	cd "${ROOT_PATH}/${CORE_NAME}"
	docker compose down
}

#######################################################################################
#  RUN COMMANDS
#######################################################################################

function run(){
    echo "Run: "${NAME_OF[$1]}""

    target_path="${FOLDER_PROJECTS_PATH}/"${NAME_OF[$1]}"/target"
    cd $target_path

    jarfile=$(ls "${NAME_OF[$1]}"*.jar)
	java_command="java -jar "${target_path}/${jarfile}" --server.port="${PORT_OF[$1]}" "${ARGS_FOR_JAVA_OF[$1]}""
    echo "- Exec: ${java_command}"

	gnome-terminal  --tab --title="${NAME_OF[$1]}" -- \
    bash -c "\
    ${java_command};
    exec bash" 
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

while getopts ":r:s:t" option; do
   case $option in
		r)  
			run "$OPTARG"
			;;
		s)
			stop "$OPTARG"
			;;	
		\?) 
			echo "Error: Invalid option"
			exit;;
   esac
done
