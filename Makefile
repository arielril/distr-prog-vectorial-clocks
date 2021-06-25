PID=0

start:
	@python ./data/starter.py 

run:
	@python ./data/index.py -c data/config --id $(PID)
