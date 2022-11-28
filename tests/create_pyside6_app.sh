# TARGET=hello_pyside6.py
TARGET=$1
NAME=`basename -s .py ${TARGET}`
PLUGIN=pyside6


virtualenv buildenv && \
	source buildenv/bin/activate && \
	cd buildenv && \
	pip install PySide6 nuitka ordered-set && \
	python ${TARGET} && \
	nuitka3 --standalone  --onefile --enable-plugin=${PLUGIN} \
			--macos-create-app-bundle ${TARGET} && \
	deactivate
