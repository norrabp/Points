#!/usr/bin/env python
""" Run the unit tests for the application"""
import coverage
import unittest
from tests import suite
COV = coverage.coverage()
COV.start()

unittest.TextTestRunner(verbosity=2).run(suite)

COV.stop()
COV.report()