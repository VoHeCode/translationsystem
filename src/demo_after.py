#!/usr/bin/env python3
# *_* coding: utf-8 *_*

"""
this is a demo.py file which repesent the code someone has writen without any translation

in this case we changed te strings that should be translatet
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
# if you use the right method it is easy to do:
# first import the translator
from translator import TranslationSystem
# and add this line
ts = TranslationSystem()
# then init it with the right locale_countrycode  de_DE en_US fr_FR etc.
ts.set_locale("de_DE")
# then only, when you have translateable stings in your file or any time after
# that you want to setup the strings to translate uncommend and run the following 2 lines
#ts.run_tr_extractor_ui()
#exit(0)
# bevor that edit the stings like:

def main(args=None):
    # original:
    # print("This does nothing, but looks good")
    # changed:
    print(ts.tr('This does nothing, but looks good'))
    # original
    # print("This does nothing, but looks good")
    print(ts.tr('The main is written in english, see it?'))
    astring = " is a string"
    astring += astring
    print(ts.tr("Please do not use fStrings in this case, because a string{}").format(astring))
    pass

if '__main__' == __name__:
    main(sys.argv)