# localbus - A simplistic python IPC package

The goal of this package is to make it very simple for several python processes to exchange information. Just register a callback for receiving stuff and, if you want to send something, call send("something").

When a message is sent, it is distributed to all connected parties but not to the sender (no loopback). Messages are strings (binary stuff has to be escaped) and, when encoded, can up to 1020 bytes long (4 bytes are used for framing). Longer messages are discarded.

Internally, multicasts with a TTL of 0 are used to make the multicast packets stay on the host.

For now, this has only been tested on Linux and in a trusted environment and should be considered pre-Alpha quality.

## Installation

Install with Pip:

```bash
pip install localbus
```

## Usage

```python
#!/usr/bin/env python3

import localbus
import signal
import sys

def signal_handler(signal, frame):
    bus.stop()
    sys.exit(0)

def recv(message: str):
    print("receive:", message)

bus = localbus.Bus(recv)
signal.signal(signal.SIGINT, signal_handler)

while True:
    input = sys.stdin.readline()
    bus.send(input.rstrip())
```

If you start two instances of this example program, they will (hopefully;-) be able to communicate with each other.

## Performance

Thousands of messages and > 10 MBit/s per second should easily be reachable (i reached 30k messages per second or ~30 MBit/s on my little test box). This is not yet tuned for performance but used with simple, text-based protocols.

