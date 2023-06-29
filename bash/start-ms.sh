#!/bin/bash

ROOT_PATH="/home/matheusmonteiro/Documents/Projetos"
CORE_NAME="shared-course-api"
ORCH_NAME="candidate-orchestrator-api"
IES_NAME="shared-institution-api"

CORE_PORT="8090"
ORCH_PORT="8094"
IES_PORT="8095"

function stopCore(){
	fuser -k ${CORE_PORT}/tcp
}

function stopOrch(){
	fuser -k ${ORCH_PORT}/tcp
}

function stopIes(){
	fuser -k ${IES_PORT}/tcp
}

function stopGateway(){
	fuser -k 8080/tcp
	docker ps --filter name=krakend* --filter status=running -aq | xargs -r docker stop
}
function stopDb(){
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

function runDb(){
	cd "${ROOT_PATH}/${CORE_NAME}"
	docker compose up -d
}

function runCore(){
	cd "${ROOT_PATH}/${CORE_NAME}"
	gnome-terminal  --tab --title=${CORE_NAME} -- bash -c "mvn -DskipTests=true clean install; java -jar "${ROOT_PATH}/${CORE_NAME}/target/${CORE_NAME}-1.0-SNAPSHOT.jar" --server.port=${CORE_PORT} --institution.baseurl=http://localhost:${IES_PORT}" 
}

function runOrch(){
	cd "${ROOT_PATH}/${ORCH_NAME}"
	gnome-terminal --tab --title=${ORCH_NAME} -- bash -c "mvn -DskipTests=true clean install; java -jar "${ROOT_PATH}/${ORCH_NAME}/target/${ORCH_NAME}-1.0-SNAPSHOT.jar" --server.port=${ORCH_PORT}" 
}

function runIes(){
	cd "${ROOT_PATH}/${IES_NAME}"
	gnome-terminal  --tab --title=${IES_NAME} -- bash -c "mvn -DskipTests=true clean install; java -jar "${ROOT_PATH}/${IES_NAME}/target/${IES_NAME}-1.0.0-SNAPSHOT.jar" --server.port=${IES_PORT}"
}

function runGateway(){
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

for ARG in $*; do
	case $ARG in
	   "-h") echo -e "==========\ns commands - for stop\n==========\n-sa stop all\n-sc stop core\n-so stop orchestrator\n-sg stop gateway\n-si stop institutions\n-sdb stop database\n==========\nr commands - for run\n==========\n-ra run all\n-rc run core\n-ro run orchestrator\n-rg run gateway\n-ri run institutions\n-rdb run database\n"
	         ;;
	   "-sa") stopAll
	         ;;
	   "-sc") stopCore
	         ;;
	   "-so") stopOrch
	         ;;
	   "-sg") stopGateway
	         ;;
	   "-sdb") stopDb
	         ;;
	   "-si") stopIes
	         ;;
	   "-ra") runAll  
	         ;;
	   "-rc") runCore  
	         ;;
	   "-ro") runOrch  
	         ;;
	   "-ri") runIes  
	         ;;
	   "-rdb") runDb
	         ;;
	   "-rg") runGateway  
	         ;;
	   *) echo -e "Comando inexistente"
	      ;;
	esac
done
exit 1
