# TARGET=hello_qt5.py
TARGET=$1
NAME=`basename -s .py ${TARGET}`
PLUGIN=pyqt5


virtualenv buildenv && \
	source buildenv/bin/activate && \
	cd buildenv && \
	pip install pyqt5 nuitka ordered-set && \
	python ${TARGET} && \
	nuitka3 --standalone  --onefile --enable-plugin=${PLUGIN} \
			--macos-create-app-bundle ${TARGET} && \
	deactivate
