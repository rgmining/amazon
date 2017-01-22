#
# amazon.py
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
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
# pylint: disable=invalid-name
"""This module provides a loading function of an Amazon Dataset.

The dataset consists of reviews for products insix categories.
The list of the categoris are defined :data:`CATEGORIES`.
If you give one or a list of categories chosed from the list to :meth:`load`,
the function will load only reviews for products belong to the given categories.

This package also provides a helper function, :meth:`print_state`,
to output a state of a graph object.

To use both fuctions, the graph object must implement the
:ref:`graph interface <dataset-io:graph-interface>`.

This is statistics of ratings and the number of reviewers:

============= ========================
Rating score  The number of reviewers
============= ========================
1.0           26754
2.0           16964
3.0           20294
4.0           57011
5.0           148373
============= ========================
"""
from __future__ import division
import datetime
import json
from os.path import exists, join
import site
import sys
import zipfile


_DATE_FORMAT = "%B %d, %Y"
"""Data format in the dataset.
"""

CATEGORIES = [
    "cameras", "laptops", "mobilephone", "tablets", "TVs", "video_surveillance"]
"""Categories this dataset has.
"""

def load(graph, categories=None):
    """Load the Amazon dataset to a given graph object.

    The graph object must implement the
    :ref:`graph interface <dataset-io:graph-interface>`.

    If a list of categories is given, only reviews which belong to one of the
    given categories are added to the graph.

    Args:
      graph: an instance of bipartite graph.

    Returns:
      The graph instance *graph*.
    """
    if categories and isinstance(categories, (list, tuple)):
        categories = list(categories)

    base = "AmazonReviews.zip"
    path = join(".", base)
    if not exists(path):
        path = join(sys.prefix, "rgmining", "data", base)
    if not exists(path):
        path = join(sys.prefix, "local", "rgmining", "data", base)
    if not exists(path):
        path = join(site.getuserbase(), "rgmining", "data", base)

    R = {}  # Reviewers dict.
    with zipfile.ZipFile(path) as archive:

        for info in archive.infolist():
            if not info.file_size:
                continue

            if categories:
                category = info.filename.split("/")[0]
                if category not in categories:
                    continue

            with archive.open(info) as fp:
                obj = json.load(fp)

                target = obj["ProductInfo"]["ProductID"]
                # To prevent adding product without any reviews,
                # create a product object before adding at least one review.
                product = None

                for r in obj["Reviews"]:
                    name = r["ReviewID"]
                    try:
                        score = (float(r["Overall"]) - 1) / 4
                    except ValueError:
                        continue

                    date = r["Date"]
                    if date:
                        try:
                            date = datetime.datetime.strptime(
                                r["Date"], _DATE_FORMAT).strftime("%Y%m%d")
                        except ValueError:
                            pass

                    if not product:
                        product = graph.new_product(name=target)

                    if name not in R:
                        R[name] = graph.new_reviewer(name=name)
                    graph.add_review(R[name], product, score, date)

    return graph


def print_state(g, i, output=sys.stdout):
    """Print a current state of a given graph.

    This method outputs a current of a graph as a set of json objects.
    Graph objects must have two properties, `reviewers` and `products`.
    Those properties returns a set of reviewers and products respectively.
    See the :ref:`graph interface <dataset-io:graph-interface>`
    for more information.

    In this output format, each line represents a reviewer or product object.

    Reviewer objects are defined as ::

        {
           "iteration": <the iteration number given as i>
           "reviewer":
           {
              "reviewer_id": <Reviewer's ID>
              "score": <Anomalous score of the reviewer>
           }
        }

    Product objects are defined as ::

        {
           "iteration": <the iteration number given as i>
           "reviewer":
           {
              "product_id": <Product's ID>
              "sumarry": <Summary of the reviews for the product>
           }
        }

    Args:
      g: Graph instance.
      i: Iteration number.
      output: A writable object (default: sys.stdout).
    """
    for r in g.reviewers:
        json.dump({
            "iteration": i,
            "reviewer": {
                "reviewer_id": r.name,
                "score": r.anomalous_score
            }
        }, output)
        output.write("\n")

    for p in g.products:
        json.dump({
            "iteration": i,
            "product": {
                "product_id": p.name,
                "summary": float(str(p.summary))
            }
        }, output)
        output.write("\n")
