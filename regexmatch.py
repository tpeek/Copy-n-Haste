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

from
([\w\W\s].*)



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

-----------------more test--------------

import re

txt='this is a paragraph with<[1> in between</[1> and then there are cases ... where the<[99> number ranges from 1-100</[99>.  and there are many other lines in the txt files with<[3> such tags </[3>'

out = re.sub("(<[^>]+>)", '', txt)
print out


------

replace whitespace

import re

txt='this is a paragraph with<[1> in between</[1> and then there are cases ... where the<[99> number ranges from 1-100</[99>.  and there are many other lines in the txt files with<[3> such tags </[3>'

out = re.sub("(<[^>]+>)", '', txt)
print out

--------       test comments


import re

txt="#om 1-100</[99>.  and there are many other lines in the txt"

out = re.sub("#([\w\W\s].*)", '', txt)
print out


--------       test docssting

import re

txt='"""this is a fucken docstring"""'

out = re.sub(""""([\w\W\s]+)""", '', txt)
print out



--------       test imports


import re

txt="import your mom"

out = re.sub("import([\w\W\s].*)", '', txt)
print out

--------       test from imports


import re

txt="from your mom i got nothen"
print txt

out = re.sub("from([\w\W\s].*)", '', txt)
print out


