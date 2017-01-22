:description: Six Categories of Amazon Product Reviews loader for
  the Review Graph Mining project. The dataset was provided by Dr. Wang.

.. _top:

Six Categories of Amazon Product Reviews Loader
==================================================
.. raw:: html

   <div class="addthis_inline_share_toolbox"></div>

For the :ref:`Review Graph Mining project <project:top>`,
this package provides a loader of the
`Six Categories of Amazon Product Reviews <http://times.cs.uiuc.edu/~wang296/Data/>`_
provided by `Dr. Wang <http://www.cs.virginia.edu/~hw5x/>`_.


Installation
--------------
Use pip to install this package.

.. code-block:: bash

  $ pip install --upgrade rgmining-amazon-dataset

Note that this installation will download a big data file from
the `original web site <http://times.cs.uiuc.edu/~wang296/Data/>`_.


Usage
------
This package provides module :mod:`amazon` and this module provides
function :meth:`amazon.load`.
The function ``load`` takes a graph object which implements
the :ref:`graph interface <dataset-io:graph-interface>`
defined in :ref:`Review Graph Mining project <project:top>`.
The funciton ``load`` also takes an optional argument, a list of categories.
If this argument is given, only reviews for products which belong to the given
categories will be loaded.

For example, the following code constructs a graph object provides the
`FRAUDAR <http://www.kdd.org/kdd2016/subtopic/view/fraudar-bounding-graph-fraud-in-the-face-of-camouflage>`_ algorithm,
loads the Six Categories of Amazon Product Reviews dataset, runs the algorithm,
and then outputs names of anomalous reviewers.
Since this dataset consists of huge reviews, loading may take long time.

.. code-block:: py

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

Note that you may need to install the
:ref:`FRAUDAR algorithm for the Review Mining Project <fraudar:top>` by

.. code-block:: bash

  pip install rgmining-fraudar


API Reference
---------------
.. toctree::
  :maxdepth: 2

  modules/amazon


License
---------
This software is released under The GNU General Public License Version 3,
see `COPYING <https://github.com/rgmining/amazon/blob/master/COPYING>`_ for more detail.

The authors of the Six Categories of Amazon Product Reviews dataset,
which this software imports, requires to cite the following papers
when you publish research papers using this package:

* `Hongning Wang`_, `Yue Lu`_, and `ChengXiang Zhai`_,
  "|pdf| `Latent Aspect Rating Analysis without Aspect Keyword Supervision <http://times.cs.uiuc.edu/~wang296/paper/p618.pdf>`_,"
  In Proc. of the 17th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD'2011),
  pp.618-626, 2011;
* `Hongning Wang`_, `Yue Lu`_, and `Chengxiang Zhai`_,
  "|pdf| `Latent Aspect Rating Analysis on Review Text Data: A Rating Regression Approach <http://sifaka.cs.uiuc.edu/~wang296/paper/rp166f-wang.pdf>`_,"
  In Proc. of the 16th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD'2010),
  pp.783-792, 2010.


.. _Hongning Wang: http://www.cs.virginia.edu/~hw5x/
.. _Yue Lu: https://www.linkedin.com/in/yue-lu-80a6a549
.. _ChengXiang Zhai: http://czhai.cs.illinois.edu/

.. |pdf| raw:: html

   <i class="fa fa-file-pdf-o" aria-hidden="true"></i>
