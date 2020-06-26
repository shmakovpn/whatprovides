Usage examples
==============

For case sensitive search:

 .. code-block:: bash

  python whatprovides.py SomeThing

For case insensitive search:

 .. code-block:: bash

  python whatprovides.py -i something

Also, you can search by a regex pattern

 .. code-block:: bash

  python whatprovides.py -r 'SomeT[a-z]ing'

Or, by a regex pattern case insensitive

 .. code-block:: bash

  python whatprovides.py -ri 'somet[a-z]ing'