import url

x = url.URL('http://username:password@www.example.co.uk:80/path/to/file?query=parameter&foo=bar#link')

if x.protocol != 'http':
    print 'protocol is broken'

if x.username != 'username':
    print 'username is broken'

if x.password != 'password':
    print 'password is broken'

if x.hostname != 'www.example.co.uk':
    print 'hostname is broken'

if x.subdomain != 'www':
    print 'subdomain is broken'

if x.domain != 'example.co.uk':
    print 'domain is broken'

if x.tld != 'uk':
    print 'tld is broken'

if x.sld != 'co':
    print x.sld + 'sld is broken'

if x.port != '80':
    print 'port is broken'

if x.path != '/path/to/file':
    print x.path + 'path is broken'

if x.query != 'query=parameter&foo=bar':
    print 'query is broken'

if x.get_query() != 'query=parameter&foo=bar':
    print 'get_query() is broken'

if x.get_query('foo') != 'bar':
    print 'qet_query(value) is broken'

if x.fragment != 'link':
    print 'fragment is broken'

if x.url != 'http://username:password@www.example.co.uk:80/path/to/file?query=parameter&foo=bar#link':
    print 'url is broken'

if x.is_subdomain_of('example.co.uk') != True:
    print 'is_subdomain_of is broken'
