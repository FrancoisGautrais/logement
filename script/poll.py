#!/bin/env python3

import sys
from datetime import datetime
from pathlib import Path

import requests
x = requests.get(sys.argv[1])
print(x.content.decode())
(Path(__file__).parent.parent / "poll.done").write_text(str(datetime.now()))