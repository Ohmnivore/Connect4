This is a simple expirement involving UniCurses for Python.
I wanted to build a nice application that can run in-terminal.

This is connect-4 (yes, the classic game) that can be played
online through TCP. It should work on all platforms, but I've
only tested it on Windows.

Usage:
  connect4.py server <address> <port>
  connect4.py client <address> <port>
  connect4.py (-h | --help)

Examples:
  connect4.py server 127.0.0.1 6666
  connect4.py client 127.0.0.1 6666

Options:
  -h, --help

Credits to:
docopt - cool command line argument/option/command parsing
UniCurses - displays stuff to the terminal
PDCurses - makes UniCurses work on Windows
Python, especially sockets

There's lots of stuff I could implement, like chat, beep
on move, move timer, first move requesting, etc., but I'll
leave that for another day.