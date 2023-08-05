YOU:
	echo "make"

lint:
	bash lint.sh mySweetCache
	bash lint.sh tests

clean:
	python3 clear_jupyter.py 
