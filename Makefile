

.PHONY: setup build run clean

all: build

build:
	sudo docker build -t reverseroski .

run:
	./venv/bin/python dev.py

setup:
	[ -d venv ] && make clean || true
	pip3 install virtualenv
	virtualenv -p `which python3` venv
	./venv/bin/pip3 install -r requirements.txt

clean:
	rm -rf venv
	echo 'y' | docker system prune
	docker rmi reverseroski
