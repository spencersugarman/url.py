import unittest
from url import URL

class TestUrlComponents(unittest.TestCase):

    def setUp(self):
        self.url = URL('http://username:password@www.example.co.uk:80/path/to/file.ext?query=parameter&foo=bar#link')

    def test_protocol(self):
        self.assertEqual(self.url.protocol, 'http')

    def test_username(self):
        self.assertEqual(self.url.username, 'username')

    def test_password(self):
        self.assertEqual(self.url.password,'password')

    def test_hostname(self):
        self.assertEqual(self.url.hostname,'www.example.co.uk')

    def test_subdomain(self):
        self.assertEqual(self.url.subdomain,'www')

    def test_domain(self):
        self.assertEqual(self.url.domain,'example.co.uk')

    def test_tld(self):
        self.assertEqual(self.url.tld,'uk')

    def test_sld(self):
        self.assertEqual(self.url.sld,'co')

    def test_port(self):
        self.assertEqual(self.url.port,'80')

    def test_path(self):
        self.assertEqual(self.url.path,'/path/to/file.ext')

    def test_dirname(self):
        self.assertEqual(self.url.dirname,'/path/to/')

    def test_basename(self):
        self.assertEqual(self.url.basename,'file.ext')

    def test_hostname(self):
        self.assertEqual(self.url.hostname, 'www.example.co.uk')

    def test_filename(self):
        self.assertEqual(self.url.filename,'file')

    def test_extension(self):
        self.assertEqual(self.url.extension,'ext')

    def test_query(self):
        self.assertEqual(self.url.query, 'query=parameter&foo=bar')

    def test_fragment(self):
        self.assertEqual(self.url.fragment, 'link')

    def test_url(self):
        self.assertEqual(self.url.url, 'http://username:password@www.example.co.uk:80/path/to/file.ext?query=parameter&foo=bar#link')

class TestUrlMethods(unittest.TestCase):

    def setUp(self):
        self.url = URL('sub.example.co.uk/path/to/file.ext?query=parameter&foo=bar')

    def test_set_path(self):
        self.url.path = 'path/to/file.ext'
        self.assertEqual(self.url.path, '/path/to/file.ext')

    def test_set_basename(self):
        self.url.basename = 'newfile.ext'
        self.assertEqual(self.url.path, '/path/to/newfile.ext')

    def test_get_query(self):
        self.assertEqual(self.url.get_query(), 'query=parameter&foo=bar')

    def test_get_single_query(self):
        self.assertEqual(self.url.get_query('foo'), 'bar')

    def test_update_query(self):
        self.url.update_query('biz', 'bazz')
        self.assertEqual(self.url.get_query('biz'), 'bazz')

    def test_overwrite_query(self):
        self.url.update_query('biz', 'booz')
        self.assertEqual(self.url.get_query('biz'), 'booz')

    def test_return_updated_query(self):
        self.url.update_query('biz', 'booz')
        self.assertEqual(self.url.query, 'query=parameter&foo=bar&biz=booz')        

    def test_is_subdomain_of(self):
        self.assertEqual(self.url.is_subdomain_of('example.co.uk'), True)

    def test_is_sub_subdomain_of(self):
        self.url = URL('http://dev.front1.example.co.uk')
        self.assertEqual(self.url.is_subdomain_of('front1.example.co.uk'), True)

    def test_is_parent_domain_of(self):
        self.assertEqual(self.url.is_parent_domain_of('dev1.sub.example.co.uk'), True)

    def test_move_up_level(self):
        self.url.move_up_level()
        self.assertEqual(self.url.path, '/path/')

    def test_move_up_to_top_level(self):
        self.url.move_up_level()
        self.url.move_up_level()
        self.url.move_up_level()
        self.assertEqual(self.url.path, '/')

    def test_validate(self):
        self.assertEqual(self.url.validate(self.url.url), True)

    def test_validate_fails(self):
        self.assertEqual(self.url.validate('h://test'), False)

class TestSettings(unittest.TestCase):

    def test_defaults(self):
        self.url = URL('front1.example.co.uk', useDefaults=True)
        self.assertEqual(self.url.url, 'http://front1.example.co.uk:80/')

    def test_file_ext_optional(self):
        self.url = URL('example.com/path/to/index', fileExtensionOptional=True)
        self.assertEqual(self.url.path, '/path/to/index')
        self.url.move_up_level()
        self.assertEqual(self.url.path, '/path/')

if __name__ == '__main__':
    unittest.main()