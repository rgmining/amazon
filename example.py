#! /usr/bin/env python
#
# example.py
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
# along with rgmining-amazon-dataset.  If not, see <http://www.gnu.org/licenses/>.
#
"""Evaluate a review graph mining algorithm with the amazon dataset.
"""
# pylint: disable=invalid-name
from __future__ import absolute_import, division
import logging
from logging import getLogger
import sys

import dsargparse
import amazon

LOGGER = getLogger(__name__)

#--------------------------
# Loading algorithms
#--------------------------
ALGORITHMS = {}
"""Dictionary of graph loading functions associated with installed algorithms.
"""

# Load and register RIA.
try:
    import ria
except ImportError:
    LOGGER.info("rgmining-ria is not installed.")
else:
    def ignore_args(func):
        """Returns a wrapped function which ignore given arguments."""
        def _(*_args):
            """The function body."""
            return func()
        return _
    ALGORITHMS["ria"] = ria.ria_graph
    ALGORITHMS["one"] = ignore_args(ria.one_graph)
    ALGORITHMS["onesum"] = ignore_args(ria.one_sum_graph)
    ALGORITHMS["mra"] = ignore_args(ria.mra_graph)


# Load and register RSD.
try:
    import rsd  # pylint: disable=wrong-import-position
except ImportError:
    LOGGER.info("rgmining-rsd is not installed.")
else:
    ALGORITHMS["rsd"] = rsd.ReviewGraph


# Load and register Fraud Eagle.
try:
    import fraud_eagle  # pylint: disable=wrong-import-position
except ImportError:
    LOGGER.info("rgmining-fraud-eagle is not installed.")
else:
    ALGORITHMS["feagle"] = fraud_eagle.ReviewGraph


# Load and register FRAUDAR.
try:
    import fraudar  # pylint: disable=wrong-import-position
except ImportError:
    LOGGER.info("rgmining-fraudar is not installed.")
else:
    def create_fraudar_graph(nblock=1):
        """Create a review graph defined in Fraud Eagle package.
        """
        return fraudar.ReviewGraph(int(nblock))
    ALGORITHMS["fraudar"] = create_fraudar_graph
#--------------------------


def run(method, loop, threshold, output, param):
    """Run a given algorithm with the Amazon dataset.

    Runs a given algorithm and outputs anomalous scores and summaries after
    each iteration finishes. The function will ends if a given number of loops
    ends or the update of one iteration becomes smaller than a given threshold.

    Some algorithm requires a set of parameters. For example, feagle requires
    parameter `epsilon`. Argument `param` specifies those parameters, and
    if you want to set 0.1 to the `epsilon`, pass `epsilon=0.1` via the
    argument.

    Args:
      method: name of algorithm.
      loop: the number of iteration (default: 20).
      threshold: threshold to judge an update is negligible (default: 10^-3).
      output: writable object where the output will be written.
      param: list of key and value pair which are connected with "=".
    """
    kwargs = {key: float(value)
              for key, value in [v.split("=") for v in param]}
    g = ALGORITHMS[method](**kwargs)
    amazon.load(g)

    amazon.print_state(g, 0, output)

    # Updates
    logging.info("Start iterations.")
    for i in xrange(loop if not method.startswith("one") else 1):

        diff = g.update()
        if diff is not None and diff < threshold:
            break

        # Current summary
        logging.info("Iteration %d ends. (diff=%s)", i + 1, diff)
        amazon.print_state(g, i + 1, output)

    # Print final state.
    amazon.print_state(g, "final", output)


def main():
    """The main function.
    """
    if not ALGORITHMS:
        logging.error("No algorithms are installed.")
        sys.exit(1)

    parser = dsargparse.ArgumentParser(main=main)
    parser.add_argument("method", choices=sorted(ALGORITHMS.keys()))
    parser.add_argument(
        "--output", default=sys.stdout,
        type=dsargparse.FileType("w"),  # pylint: disable=no-member
        help="file path to store results (Default: stdout).")
    parser.add_argument("--loop", type=int, default=20)
    parser.add_argument("--threshold", type=float, default=10^-3)
    parser.add_argument(
        "--param", action="append", default=[],
        help=(
            "key and value pair which are connected with '='.\n"
            "This option can be set multiply."))

    run(**vars(parser.parse_args()))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception:  # pylint: disable=broad-except
        logging.exception("Untracked exception occurred.")
    finally:
        logging.shutdown()
