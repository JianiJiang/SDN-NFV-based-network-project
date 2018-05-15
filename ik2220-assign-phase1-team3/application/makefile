app:
	python -m compileall ./sdn/
	PYTHONPATH=$(PWD)/sdn /opt/ik2220/pox/pox.py MyController
clean: 
	sudo killall MyController

