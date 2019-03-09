# Python
MAIN_NAME=dev.py
ENV_NAME=venv
PYTHON_VERSION=`which python3`

# Docker
DOCKER_OPTIONS=--rm -p 5000:5000
DOCKER_DEPLOY_OPTIONS=-d
DOCKER_IMAGE_NAMES=reverserooski_reverserooski mariadb traefik jmc1283/flasq-base

.PHONY: all deploy buildall buildbase build run kill clean setup debug

all: deploy
buildall: buildbase build

############################################################
#      _            _                   _          __  __  #
#   __| | ___   ___| | _____ _ __   ___| |_ _   _ / _|/ _| #
#  / _` |/ _ \ / __| |/ / _ \ '__| / __| __| | | | |_| |_  #
# | (_| | (_) | (__|   <  __/ |    \__ \ |_| |_| |  _|  _| #
#  \__,_|\___/ \___|_|\_\___|_|    |___/\__|\__,_|_| |_|   #
#                                                          #
############################################################

deploy: check_proxy
	docker-compose kill
	docker-compose rm -f
	docker-compose up --build --force-recreate ${DOCKER_DEPLOY_OPTIONS}

buildbase:
	docker build -t jmc1283/flasq-base base

run: check_proxy kill build
	docker-compose run ${DOCKER_OPTIONS} reverserooski

clean: kill
	docker system prune -f
	if [ -n "`docker image list -q | grep ${DOCKER_IMAGE_NAME}`" ]; then \
		docker rmi ${DOCKER_IMAGE_NAMES}; \
		docker rmi jmc1283/flasq-base; \
	fi
	if [ -d ${ENV_NAME} ]; then \
		rm -rf ${ENV_NAME}; \
	fi
	if [ -n "`find . -type f -name __pycache__`" ]; then \
		rm -rf `find . -type f -name __pycache__`; \
	fi
	if [ -n "`find . -type d -name .data`" ]; then \
		rm -rf `find . -type d -name .data`; \
	fi

build:
	docker-compose build

kill:
	docker-compose kill reverserooski

check_proxy:
	if [ -z "`docker network ls | grep traefik-proxy`" ]; then \
		docker network create traefik-proxy; \
	fi


##########################################################
#      _      _                       _          __  __  #
#   __| | ___| |__  _   _  __ _   ___| |_ _   _ / _|/ _| #
#  / _` |/ _ \ '_ \| | | |/ _` | / __| __| | | | |_| |_  #
# | (_| |  __/ |_) | |_| | (_| | \__ \ |_| |_| |  _|  _| #
#  \__,_|\___|_.__/ \__,_|\__, | |___/\__|\__,_|_| |_|   #
#                         |___/                          #
#																												 #
##########################################################

setup:
	if [ -d ${ENV_NAME} ]; then \
		rm -rf ${ENV_NAME}; \
	fi
	if [ -a base/requirements.txt ]; then \
		touch base/requirements.txt; \
	fi
	which virtualenv && pip install virtualenv || true
	virtualenv -p ${PYTHON_VERSION} ${ENV_NAME}
	./${ENV_NAME}/bin/pip install -r base/requirements.txt
	./${ENV_NAME}/bin/pip install -r requirements.txt

debug:
	if [ ! -d ${ENV_NAME} ]; then \
		make setup; \
	fi
	if [ ! -e web/.data ]; then \
		mkdir web/.data; \
	fi
	./${ENV_NAME}/bin/python3 -c "from web import db; db.create_all()"
	./${ENV_NAME}/bin/python ${MAIN_NAME}
