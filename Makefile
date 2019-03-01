generate-setup-file:
	py2applet --make-setup client.py --iconfile icon.icns

build-macosapp:
	rm -rf build dist && python3 setup.py py2app -A

build-client-executable:
	pyinstaller client.py

build-server-executable:
	pyinstaller server.py