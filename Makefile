build:
	pyside6-rcc qml/resources.qrc -o qml/resources_rc.py

run: build
	python main.py
