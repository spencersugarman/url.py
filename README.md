url.py
======
A teeny tiny itty bitty Python library for extracting and manipulating URLs.

Passing a URL to url.py breaks apart the URL into its component parts:

* Protocol ('http')
* Subdomain ('www')
* Domain ('example.co.uk')
* Top Level Domain ('uk')
* Second Level Domain ('co')
* Hostname ('www.example.co.uk')
* Port ('80')
* Path ('/pages/about/')
* Query ('?user=dan&redirect=1')
* Fragment ('#link')

These can be accessed at myUrl.protocol, myUrl.subdomain, and so on.

Other fun things you can do:

**add_query(queryName, parameter)**

**update_query(queryName, parameter)**

**delete_query(queryName)**

**get_query([queryName])**

**get_queries()**

**move_up_level()**

**is_subdomain_of(testUrl)**
