#!/bin/env python3

import sys
import requests
x = requests.get(sys.argv[1])
print(x.content.decode())