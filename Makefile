ifndef VERBOSE
.SILENT:
endif

runloop:
	while find -type f -path './data/*.py' -print | \
	    xargs inotifywait -qq -e 'close_write,close'; do \
		sleep 0.1; clear; make run; \
	done
run:
	python3 asteroids.py

clean: cleanvim cleanpy

cleanvim:
	find . -type f \( -name '*~' -o -name '*.swp' \) -delete

cleanpy:
	find . \( -name '__pycache__' -o -name '*.pyc' \) -delete

ctags:
	ctags -R
