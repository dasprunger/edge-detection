__author__ = 'dasprunger'

import unittest
import edgefinder


class VertEdgeTests(unittest.TestCase):
    def test_find_vert_edges(self):
        edge_array = edgefinder.find_horizontal_edges("scope_32.png")

