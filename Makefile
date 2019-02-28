generate-setup-file:
	py2applet --make-setup client.py --iconfile icon.icns

build:
	rm -rf build dist && python3 setup.py py2app -A