import unittest
import os

loader = unittest.TestLoader()
start_dir = os.getcwd() + '/tests/cases/'
suite = loader.discover(start_dir)
