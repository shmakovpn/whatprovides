Usage examples
==============

For case sensitive search:

 .. code-block:: bash

  whatprovides.py SomeThing

For case insensitive search:

 .. code-block:: bash

  whatprovides.py -i something

Also, you can search by a regex pattern

 .. code-block:: bash

  whatprovides.py -r 'SomeT[a-z]ing'

Or, by a regex pattern case insensitive

 .. code-block:: bash

  whatprovides.py -ri 'somet[a-z]ing'

Output can be filtered to show only classes (-c), only functions (-d) or variables (-v).
To show classes and functions without variables use (-cd).
(-cv) show classes and variables. (-dv) show functions and variables.

Getting help:

 .. code-block:: bash

  whatprovides.py --help


