arduino-serial-plotter.pex: server
	 pex flask pyserial gevent . -m server.server:main -o dist/arduino-serial-plotter.pex -v

clean:
	rm *.pex

.PHONY: clean
