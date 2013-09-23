url.py
======
A teeny tiny itty bitty Python library for extracting and manipulating URLs.

_Covers about 1.36% of http://tools.ietf.org/html/rfc3986_

## Properties

Passing a URL to url.py breaks apart the URL into its component parts:

* Protocol ('http')
* Username/Password ('myname:mypassword@')
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

## Methods

Other fun things you can do:

### update_query(queryName, parameter)

Add a key/value pair to the query string.

    myUrl = URL('http://example.com/?q1=p1')
    myUrl.update_query('newQuery', 'newParam')
    myUrl.url # http://example.com/?q1=p1&newQuery=newParam
    
If a query with that name already exists, its parameter is updated:

    myUrl.url # http://example.com/?q1=p1&newQuery=newParam
    myUrl.update_query('newQuery', 'reallyNewParam')
    myUrl.url # http://example.com/?q1=p1&newQuery=reallyNewParam
    
### delete_query(queryName)

Remove a query with the given name from the query string

    myUrl.url # http://example.com/?q1=p1&newQuery=reallyNewParam
    myUrl.delete_query('newQuery')
    myUrl.url # http://example.com/?q1=p1

### get_query([queryName])

Get the query string. If no queryName is specified, returns the same as myUrl.query.

    myUrl.url # http://example.com/?q1=p1
    myUrl.get_query # q1=p1
    
If a queryName is specified, returns that part of the query string only:

    myUrl.url # http://example.com/?q1=p1&newQuery=reallyNewParam
    myUrl.get_query('q1') # q1=p1
    myUrl.get_query('newQuery') # newQuery=reallyNewParam

### get_queries()

Returns the queries string as a dictionary.

    myUrl.url # http://example.com/?q1=p1&newQuery=reallyNewParam
    myURL.get_queries() # {
                        #   "q1":"p1"
                        #   "newQuery":"reallyNewParam"
                        # }

### move_up_level([numLevels])

Moves up the path by the specified number of levels (defaults to 1) 

    myUrl.url # http://example.com/pages/about/dan/
    myUrl.move_up_level()
    myUrl.url # http://example.com/pages/about/
    myUrl.move_up_level(2)
    myUrl.url # http://example.com/

### is_subdomain_of(testUrl)

Tests if your URL is a subdomain of the passed URL.

    myUrl.url # http://stage.host1.example.com/
    myUrl.is_subdomain_of('host1.example.com') # True
    myUrl.is_subdomain_of('example.com') # True
    myUrl.is_subdomain_of('www.example.com') # False

### is_parent_domain_of(testUrl)

Tests if your URL is a parent domain of the passed URL.

    myUrl.url # example.com
    myUrl.is_parent_domain_of('http://stage.host1.example.com/') # True
    myUrl.is_parent_domain_of('www.example.com/') # True
    myUrl.is_parent_domain_of('http://example.com') # False
