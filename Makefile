# Python
MAIN_NAME=reverseroski
ENV_NAME=venv
PYTHON_VERSION=/usr/bin/python3

# Docker
DOCKER_IMAGE_NAME=reverseroski
DOCKER_OPTIONS=--rm -it -p 5000:5000
DOCKER=sudo docker

.PHONY: run setup build rund killd clean cleand

all: build

build:
	${DOCKER} build -t ${DOCKER_IMAGE_NAME} .

rund: killd
	${DOCKER} run ${DOCKER_OPTIONS} --name ${DOCKER_IMAGE_NAME} ${DOCKER_IMAGE_NAME}

killd:
	@if [ -n "$(${DOCKER} ps -q) | grep ${DOCKER_IMAGE_NAME}" ]; then \
		${DOCKER} kill ${DOCKER_IMAGE_NAME}; \
	fi

setup:
	@if [ -d ${ENV_NAME} ]; then \
		rm -rf ${ENV_NAME}; \
	fi
	@if [ -a requirements.txt ]; then \
		touch requirements.txt; \
	fi
	pip install virtualenv
	virtualenv -p ${PYTHON_VERSION} ${ENV_NAME}
	./${ENV_NAME}/bin/pip install -r requirements.txt

run: 
	@if [ -d ${ENV_NAME} ]; then \
		make setup; \
	fi
	./${ENV_NAME}/bin/python ${MAIN_NAME}

cleand: killd
	echo 'y' | ${DOCKER} system prune
	${DOCKER} rmi ${DOCKER_IMAGE_NAME}

clean:
	@if [ -d ${ENV_NAME} ]; then \
		rm -rf ${ENV_NAME}; \
	fi
