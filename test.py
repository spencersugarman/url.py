from url import URL

x = URL('http://username:password@www.example.co.uk:80/path/to/file.ext?query=parameter&foo=bar#link')

if x.protocol != 'http':
    print x.protocol + ' protocol is broken'

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
    print x.sld + ' sld is broken'

if x.port != '80':
    print 'port is broken'

if x.path != '/path/to/file.ext':
    print x.path + ' path is broken'

if x.dirname != '/path/to/':
    print x.dirname + ' dirname is broken'
if x.basename != 'file.ext':
    print x.basename + ' basename is broken'
if x.filename != 'file':
    print x.filename + ' filename is broken'
if x.extension != 'ext':
    print x.extension + ' extension is broken'

x.path = '/'
if x.path != '/':
    print x.path + ' setting path is broken'
x.basename = 'file.ext'
if x.path != '/file.ext':
    print x.path + ' setting basename is broken'
x.path = 'path/to/file.ext'
if x.path != '/path/to/file.ext':
    print x.path + ' setting malformed path is broken'

if x.query != 'query=parameter&foo=bar':
    print 'query is broken'

if x.get_query() != 'query=parameter&foo=bar':
    print 'get_query() is broken'

if x.get_query('foo') != 'bar':
    print 'qet_query(value) is broken'

if x.fragment != 'link':
    print 'fragment is broken'

if x.url != 'http://username:password@www.example.co.uk:80/path/to/file.ext?query=parameter&foo=bar#link':
    print x.url + ' url is broken'

x.update_query('biz', 'bazz')
if x.get_query('biz') != 'bazz':
    print 'update_query is broken'

x.update_query('biz', 'booz')
if x.get_query('biz') != 'booz':
    print 'update_query overwrite is broken'

if x.is_subdomain_of('example.co.uk') != True:
    print 'is_subdomain_of is broken'

# Test is_subdomain_of method with a sub-subdomain
x2 = URL('http://dev.front1.example.co.uk')
if x2.is_subdomain_of('front1.example.co.uk') != True:
    print 'subsubdomain is_subdomain_of is broken'

# Test parent domain method
x3 = URL('front1.example.co.uk')
if x3.is_parent_domain_of('http://dev.front1.example.co.uk') != True:
    print 'is_parent_domain_of is broken'

# Test parent domain method with same domain
x4 = URL('example.co.uk')
if x4.is_parent_domain_of('http://example.co.uk') != False:
    print 'is_parent_domain_of is broken'

x5 = URL('/path/to/index.html')
if x5.hostname != None:
    print x5.hostname + ' hostname for relative path is broken'