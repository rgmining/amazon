#
# amazon_test.py
#
# Copyright (c) 2017 Junpei Kawamoto
#
# This file is part of rgmining-amazon-dataset.
#
# rgmining-amazon-dataset is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# rgmining-amazon-dataset is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with rgmining-amazon-dataset. If not, see <http://www.gnu.org/licenses/>.
#
"""Unit test for synthetic package.
"""
from collections import defaultdict
import random
import unittest
import amazon


class GraphMock(object):
    """A mock of graph object.
    """

    def __init__(self):
        self.reviewers = set()
        self.products = set()
        self.reviews = defaultdict(dict)

    def new_reviewer(self, name):
        """Create a new reviewer.
        """
        if name in self.reviewers:
            raise ValueError("The given reviewer already exists:", name)
        self.reviewers.add(name)
        return name

    def new_product(self, name):
        """Create a new product.
        """
        if name in self.products:
            raise ValueError("The given product already exists:", name)
        self.products.add(name)
        return name

    def add_review(self, reviewer, product, score, _date=None):
        """Add a review.
        """
        if reviewer not in self.reviewers:
            raise ValueError("The given reviewer doesn't exist:", reviewer)
        if product not in self.products:
            raise ValueError("The given product doesn't exist:", product)
        self.reviews[reviewer][product] = score


class TestGraphMock(unittest.TestCase):
    """Test case for the mock object.
    """

    def setUp(self):
        """Set up for the tests.
        """
        self.graph = GraphMock()

    def test_new_reviewer(self):
        """If create same reviewers, mock should rises an error.
        """
        name = "test-reviewer"
        self.assertEqual(self.graph.new_reviewer(name), name)
        with self.assertRaises(ValueError):
            self.graph.new_reviewer(name)

    def test_new_product(self):
        """If create same products, mock should rises an error.
        """
        name = "test-product"
        self.assertEqual(self.graph.new_product(name), name)
        with self.assertRaises(ValueError):
            self.graph.new_product(name)

    def test_add_review(self):
        """Test add_review method.
        """
        reviewer = "test-reviewer"
        product = "test-product"
        self.graph.new_reviewer(reviewer)
        self.graph.new_product(product)

        score = random.random()
        self.graph.add_review(reviewer, product, score)
        self.assertEqual(self.graph.reviews[reviewer][product], score)

        with self.assertRaises(ValueError):
            self.graph.add_review(reviewer, reviewer, score)
        with self.assertRaises(ValueError):
            self.graph.add_review(product, product, score)


class TestLoad(unittest.TestCase):
    """Test case for load method.
    """

    def test_load(self):
        """Test load method.
        """
        graph = GraphMock()
        self.assertEqual(amazon.load(graph), graph)

        for pmap in graph.reviews.values():
            for score in pmap.values():
                self.assertGreaterEqual(score, 0)
                self.assertLessEqual(score, 1)

    def test_load_one_category(self):
        """Test load method with one category.
        """
        graph = GraphMock()
        self.assertEqual(amazon.load(graph, amazon.CATEGORIES[0]), graph)

        for pmap in graph.reviews.values():
            for score in pmap.values():
                self.assertGreaterEqual(score, 0)
                self.assertLessEqual(score, 1)

    def test_load_two_categories(self):
        """Test load method with two categories.
        """
        graph = GraphMock()
        self.assertEqual(amazon.load(graph, amazon.CATEGORIES[2:4]), graph)

        for pmap in graph.reviews.values():
            for score in pmap.values():
                self.assertGreaterEqual(score, 0)
                self.assertLessEqual(score, 1)


if __name__ == "__main__":
    unittest.main()
