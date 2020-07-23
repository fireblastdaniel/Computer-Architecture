#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()
if len(sys.argv) < 2:
  print('Please add the path to a test file')
  exit()
else:
  test_file = sys.argv[1]

cpu.load(test_file)
cpu.run()