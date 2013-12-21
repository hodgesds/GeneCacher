GeneCacher
==========

GeneCacher
----------

Python interface to convert a fasta file into memcached data

Example
-------


```
from genecacher import tools
test = tools()
test.cache_fasta('chrM.fa')
print test.get_base('chrM',10)
print test.get_region('chrM:10-20')
test.clear_cache()
print test.get_base('chrM',10)

```
