arduino-serial-plotter.pex: server
	 pex flask . -m server.server:main -o dist/arduino-serial-plotter.pex -v --disable-cache

clean:
	rm *.pex

.PHONY: clean
