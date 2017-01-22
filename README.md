# Amazon Dataset Loader
[![GPLv3](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://www.gnu.org/copyleft/gpl.html)
[![Build Status](https://travis-ci.org/rgmining/amazon.svg?branch=master)](https://travis-ci.org/rgmining/amazon)
[![Release](https://img.shields.io/badge/release-0.5.0-brightgreen.svg)](https://github.com/rgmining/amazon/releases/tag/v0.5.0)
[![PyPi](https://img.shields.io/badge/pypi-0.5.0-brightgreen.svg)](https://pypi.python.org/pypi/rgmining-tripadvisor-dataset)

[![Logo](https://rgmining.github.io/amazon/_static/image.png)](https://rgmining.github.io/amazon/)

For the [Review Graph Mining project](https://github.com/rgmining),
this package provides a loader of the
[Six Categories of Amazon Product Reviews dataset](http://times.cs.uiuc.edu/~wang296/Data/)
provided by [Dr. Wang](http://www.cs.virginia.edu/~hw5x/).


## Installation
Use pip to install this package.

```shell
$ pip install --upgrade rgmining-amazon-dataset
```

Note that this installation will download a big data file from
the [original web site](http://times.cs.uiuc.edu/~wang296/Data/).


## Usage
This package provides module `amazon` and this module provides function `load`.
The `load` function takes a graph object which implements
the [graph interface](https://rgmining.github.io/dataset-io/modules/dataset_io.html#graph-interface)
defined in [Review Graph Mining project](https://github.com/rgmining).
The funciton `load` also takes an optional argument, a list of categories.
If this argument is given, only reviews for products which belong to the given
categories will be loaded.


For example, the following code constructs a graph object provides the
[FRAUDAR](http://www.kdd.org/kdd2016/subtopic/view/fraudar-bounding-graph-fraud-in-the-face-of-camouflage) algorithm,
loads the Amazon dataset,
runs the algorithm, and then outputs names of anomalous reviewers.
Since this dataset consists of huge reviews, loading may take long time.

```py
import fraudar
import amazon

# Construct a graph and load the dataset.
graph = fraudar.ReviewGraph()
amazon.load(graph)

# Run the analyzing algorithm.
graph.update()

# Print names of reviewers who are judged as anomalous.
for r in graph.reviewers:
  if r.anomalous_score == 1:
    print r.name

# The number of reviewers the dataset has: -> 634295.
len(graph.reviewers)

# The number of reviewers judged as anomalous: -> 91.
len([r for r in graph.reviewers if r.anomalous_score == 1])
```

Note that you may need to install the FRAUDAR algorithm for the Review Mining Project
by `pip install rgmining-fraudar`.


## License
This software is released under The GNU General Public License Version 3,
see [COPYING](COPYING) for more detail.

The authors of the Trip Advisor dataset, which this software imports, requires to
cite the following papers when you publish research papers using this package:

- [Hongning Wang](http://www.cs.virginia.edu/~hw5x/),
  [Yue Lu](https://www.linkedin.com/in/yue-lu-80a6a549),
  and [ChengXiang Zhai](http://czhai.cs.illinois.edu/),
  "[Latent Aspect Rating Analysis without Aspect Keyword Supervision](http://times.cs.uiuc.edu/~wang296/paper/p618.pdf),"
  In Proc. of the 17th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD'2011),
  pp.618-626, 2011;
- [Hongning Wang](http://www.cs.virginia.edu/~hw5x/),
  [Yue Lu](https://www.linkedin.com/in/yue-lu-80a6a549),
  and [Chengxiang Zhai](http://czhai.cs.illinois.edu/),
  "[Latent Aspect Rating Analysis on Review Text Data: A Rating Regression Approach](http://sifaka.cs.uiuc.edu/~wang296/paper/rp166f-wang.pdf),"
  In Proc. of the 16th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD'2010),
  pp.783-792, 2010.
