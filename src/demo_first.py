#!/usr/bin/env python3
# *_* coding: utf-8 *_*

"""
this is a demo.py file which repesent the code someone has writen without any translation

"""

__version__ = "1.0.0"
__author__ = "Author 1, Author 2, Author 3"  # only code writers
__email__ = "author@bogusproject.com"
__maintainer__ = "Maintainer 1"  # should be the person who will fix bugs and make improvements
__copyright__ = "Copyright 2019, Our project"
__license__ = "GPL"
__status__ = "Production"  # Prototype, Development or Production
__credits__ = ["name 1", "name 2"]  # also include contributors that wrote no code

# --------------------------------------------------------------------------------

# Import built-in modules first
# followed by third-party modules
# followed by any changes to the path
# your own modules.
import sys


def main(args=None):
    print("This does nothing, but looks good")
    print('The main is written in english, see it?')
    astring = " is a string"
    astring += astring
    print("Please do not use fStrings in this case, because a string{}".format(astring))
    pass


if '__main__' == __name__:
    main(sys.argv)
