import re

url = 'abcdc.com'
url = re.sub('\.com$', '', url)

------------------------------------finding stings------------------------------------------------

finding doctrings:
"""([\w\W\s]+)"""


finding comments
#([\w\W\s].*)

finding imports
import([\w\W\s].*)



------------------------------------------------------------------------------------
/"""([\w\W\s]+)"""/g



--------news
"""([\w\W\s]+)"""



#([\w\W\s])

"""this is a fucken docstring"""

#this is a comment hahaha

import your mom

---------------------------------reping a line---------------------------------------------------
/"""([\w\W\s]+)"""/g


import re
line = re.sub(r"</?\[\d+>", "", line)
