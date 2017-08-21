ifndef VERBOSE
.SILENT:
endif

runloop:
	while find -type f -path './data/*.py' -print | \
	    xargs inotifywait -qq -e 'close_write,close'; do \
		sleep 0.1; clear; make run; \
	done
run:
	./asteroids

test:
	nosetests tests --with-coverage --cover-erase -v -s --cover-package=data.components data.states.game
	-pyflakes .
	-pep8 .

clean: cleanvim cleanpy

cleanvim:
	find . -type f \( -name '*~' -o -name '*.swp' \) -delete

cleanpy:
	find . \( -name '__pycache__' -o -name '*.pyc' \) -delete

ctags:
	ctags -R
