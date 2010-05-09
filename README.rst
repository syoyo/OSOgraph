OSOgraph
========

.. image:: http://github.com/syoyo/OSOgraph/blob/master/test.png 

OSOgraph visualizes OSO(compiled intermediate instructions of OpenShadingLanguage by oslc) using graphviz.

Requirements
------------

 * OSL compiler from openshadinglanguage
   * http://code.google.com/p/openshadinglanguage/
 * Python
 * Graphviz


How to use
----------

::

 $ oslc test.osl
 $ python osograph.py test.oso
 $ dot -Tpng output.dot > test.png


Limitation & TODO
-----------------

A lot.

I've made this simple script just for fun and understanding oso format, thus please don't expect too much on this project ;-)


License
-------

BSD 2
