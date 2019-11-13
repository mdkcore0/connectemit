# connectemit
A very (very very very very very...) simple python signal implementation,
barely based on [Qt signals](https://doc.qt.io/qt-5/signalsandslots.html#signals).

This is not intended to be a drop-in replacement to [pyqtSignal](https://www.riverbankcomputing.com/static/Docs/PyQt5/signals_slots.html#defining-new-signals-with-pyqtsignal),
but a lightweight (and limited) alternative.

See [signalslot](https://github.com/Numergy/signalslot) for a more robust and
complete alternative.

## Requirements
- python 2.7

# Example
```python
from ce import ConnectEmit


def abc(s, i):
    print("ABC %s, %s" % (s, i))


def xyz(s, i):
    print("XYZ %s, %s" % (s, i))


emitter = ConnectEmit(str, int, arguments=['s', 'i'])
emitter.connect(abc)
emitter.connect(xyz)

emitter.emit("123", 124)
```

## TODO
This is a very (...) initial version, expect *TODO*s and *XXX*s and bugs along
the code.

Also, the following are not currently supported (but are planned):

- diconnecting from function/methods
- connecting a **ConnectEmit** instance to another one (chaining)
- documentation
- tests
- python3 (should drop 2.7)
