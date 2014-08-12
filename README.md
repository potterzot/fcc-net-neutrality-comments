fcc_netneutrality_comments
==========================

Fetch and process net neutrality comments. The comments can be processed into an HDF5 file that is over 5GB, or an sqlite3 database that is XX. 

While HDF5 can typically be very nice and fast, it has some drawbacks in this case:

1. Because HDF5 requires a string field of a specified length, the comments can't be recorded in their entirety without making the string length something like 35,000 characters (The value in the script is 10,000).

2. It doesn't play nicely with UTF-8 formatting. Some of the names contain accent characters, so the text is byte-encoded and would have to be byte-decoded for text analysis. A minor thing, but considering that sqlite does just fine interpreting accented characters, this is just another thing that you don't need to worry about.




