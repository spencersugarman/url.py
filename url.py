import re

class URL(object):
    """A class for extracting various parts of a URL"""
    def __init__ (self, value, useDefaults=False, fileExtensionOptional=False, defaults={}):
        # If useDefaults=True, protocol and port will be set to defaults if missing
        self.useDefaults = useDefaults is True
        self.defaults = {
            'protocol':'http', 
            'ports': {
                'ftp': '21',
                'http': '80',
                'https': '443'
            }
        }
        self.url = value

    def __str__(self):
        return self.url

    @property
    def url(self):
        """The url property."""
        url = ''
        if self.protocol:
            url = ''.join((self.protocol, '://'))
        if self.username:
            url = ''.join((url, self.username, ':', self.password, '@'))
        if self.hostname:
            url = ''.join((url, self.hostname))
        if self.port:
            url = ''.join((url, ':', str(self.port)))
        if self.path:
            url = ''.join((url, self.path))
        if self.query:
            url = ''.join((url, '?', self.query))
        if self.fragment:
            url = ''.join((url, '#', self.fragment))
        return url
    @url.setter
    def url(self, value):
        # in an example URL http://user:pass@www.example.co.uk:80/dir/?foo=bar#link
        parts = self._parse_url(value)
        # protocol is 'http'
        self.protocol = parts['protocol']
        # username is 'user'
        self.username = parts['username']
        # password is 'pass'
        self.password = parts['password']
        # hostname is 'www.example.co.uk'
        self.hostname = parts['hostname']
        # port is '80'
        self.port = parts['port']
        # path is '/dir/'
        self.path = parts['path']
        # query is 'foo=bar'
        self.query = parts['query']
        # fragment is 'link'
        self.fragment = parts['fragment']

    @property
    def protocol(self):
        """The protocol property."""
        return self._protocol
    @protocol.setter
    def protocol(self, value):
        if value is None:
            self._protocol = None
        else:
            match = re.match('[a-z][a-z0-9+-]*', value, re.I)
            if match is None:
                raise Exception("This is not a valid protocol")
            self._protocol = value

    @property
    def port(self):
        """The port property."""
        return self._port
    @port.setter
    def port(self, value):
        if value is None:
            if self.useDefaults and self.protocol is not None:
                if self.protocol in self.defaults['ports']:
                    self._port = self.defaults['ports'][self.protocol]
            else:
                self._port = None
        else:
            self._port = value

    @property
    def query(self):
        """The query property."""
        return self._build_query()    
    @query.setter
    def query(self, value):
        if value is None:
            self._queries = None
        else:
            self._queries = self._parse_query(value)

    @property
    def hostname(self):
        """The hostname property."""
        hostname = ''
        if self.subdomain:
            hostname = self.subdomain + '.'
        if self._domain:
            hostname += self._domain
        return hostname or None
    @hostname.setter
    def hostname(self, value):
        self._update_hostname(value)

    @property
    def domain(self):
        """The domain property."""
        return self.hostname[len(self.subdomain)+1:]
    @domain.setter
    def domain(self, value):
        self._update_hostname(value)

    @property
    def path(self):
        """The path property."""
        if self.basename is not None:
            return ''.join((self.dirname, self.basename))
        else: 
            return self.dirname
    @path.setter
    def path(self, value):
        parts = self._parse_path(value)
        self.dirname = parts['dirname']
        self.basename = parts['basename']

    @property
    def basename(self):
        """The basename property."""
        if self.extension is None:
            return self.filename
        else:
            return ''.join((self.filename, '.', self.extension))
    @basename.setter
    def basename(self, value):
        if self.dirname is None:
            self.dirname = '/'
        parts = self._parse_basename(value)
        self.filename = parts['filename']
        self.extension = parts['extension']

    def _update_hostname(self, hostname):
        parts = self._parse_hostname(hostname)
        self.subdomain = parts['subdomain']
        self._set_domain(parts)

    def _set_domain(self, parts):
        # in an example URL http://user:pass@www.example.co.uk:80/dir/?foo=bar#link
        # domain is 'example.com'
        self._domain = parts['domain']
        # top level domain is 'uk'
        self.tld = parts['tld']
        # second level domain is 'co'
        self.sld = parts['sld']

    def _parse_hostname(self, value):
        """Extract the subdomain, domain, tld, and sld"""
        parts = {'tld':None, 'sld':None, 'domain':None, 'subdomain':None}
        if value:
            pos = value.find('.')
            if pos > -1:
                xlds = self._get_xlds(value)
                parts['tld'] = xlds['tld']
                parts['sld'] = xlds['sld']
                matches = re.findall('(\.)', value)
                if len(matches) == 1 or (xlds['sld'] and len(matches) == 2):
                    # example.com
                    # example.co.uk
                    parts['domain'] = value
                else:
                    # www.example.com
                    # ww.example.co.uk
                    pos = value.find('.')
                    parts['domain'] = value[pos+1:]
                    parts['subdomain'] = value[:pos]
            else:
                parts['domain'] = value
        return parts

    def _build_query(self):
        if self._queries is not None:
            return "&".join('%s=%s' % (k, v) for k,v in self._queries.iteritems())

    def _parse_query(self, value):
        queries = {}
        splitValue = value.split('&')
        for query in splitValue:
            pos = query.find('=')
            queries[query[:pos]] = query[pos+1:]
        return queries

    def update_query(self, query, parameter):
        """Updates a parameter in the query string;

        Overwrites current parameter if passed an existing query

        """
        self._queries[query] = parameter

    def delete_query(self, query):
        """Deletes a query from the query string"""
        self._queries.pop(query, None)

    def get_query(self, query=None):
        """Convenience method for returning the entire query string or specific query"""
        if query is None:
            return self._build_query()
        return self._queries[query]

    def qet_queries(self):
        """Returns the query string as a dictionary"""
        return self._queries
        
    def _parse_path(self, value):
        """Returns a dict with the dirname and basename of the passed value"""
        parts = {}
        if value:
            if value[0] != '/':
                value = '/' + value
            pos = value.rfind('/')
            if pos > -1:
                parts['dirname'] = value[:pos+1]
                parts['basename'] = value[pos+1:]
        else:
            parts['dirname'] = '/'
            parts['basename'] = None
        return parts

    def _parse_basename(self, value):
        """Returns a dict with the filename and extension of the passed value"""
        parts = {}
        if value:
            pos = value.rfind('.')
            if pos > -1:
                parts['filename'] = value[:pos]
                parts['extension'] = value[pos+1:]
            elif self.fileExtensionOptional == True:
                parts['filename'] = value
                parts['extension'] = None
        else:
            parts['filename'] = None
            parts['extension'] = None
        return parts

    def move_up_level(self, numLevels=1):
        """Moves the URL path up one level in the directory tree;

        recurses if numLevels is greater than 1

        """
        # if at /path/to/level1/level2/
        # move_up_dir() will return /path/to/level1/
        if numLevels > 0 and self.dirname and len(re.findall('/', self.dirname)):
            pos = self.dirname[:-1].rfind('/')
            self.path = self.dirname[:pos+1]
            if numLevels > 1:
                self.move_up_level(numLevels - 1)

    def is_subdomain_of(self, testUrl):
        """Returns True if Object.url is subdomain of the passed URL"""
        parts = self._parse_url(testUrl)
        return self.subdomain and self.hostname.find(parts['hostname']) > -1

    def is_parent_domain_of(self, testUrl):
        """Returns True if Object.url is parent domain of the passed URL"""
        parts = self._parse_url(testUrl)
        testHostname = parts['hostname']
        if testHostname is not None:
            testHostnameParts = self._parse_hostname(testHostname)
            testSubdomain = testHostnameParts['subdomain']
            if testSubdomain is not None:
                # test URL must have subdomain to have a parent domain
                return testHostname.find(self.hostname) > -1
        return False

    def _parse_url(self, value):
        parts = {}
        # http://username:password@www.example.com:80/path/to/file?query=parameter#link
        pos = value.find('#')
        if pos > -1:
            parts['fragment'] = value[pos+1:]
            value = value[:pos]
        else:
            parts['fragment'] = None

        # http://username:password@www.example.com:80/path/to/file?query=parameter
        pos = value.find('?')
        if pos > -1:
            parts['query'] = value[pos+1:]
            value = value[:pos]
        else:
            parts['query'] = None

        # http://username:password@www.example.com:80/path/to/file
        if value[0:1] == '//':
            # no scheme given
            value = value[2:]
        else:
            pos = value.find('://')
            if pos > -1:
                parts['protocol'] = value[:pos].lower()
                value = value[pos+3:]
            elif self.useDefaults:
                parts['protocol'] = self.defaults['protocol']
            else:
                parts['protocol'] = None

        # username:password@www.example.com:80/path/to/file
        pos = value.find('@')
        if pos > -1 and pos < value.find('/'):
            userinfo = value[:pos].split(':')
            parts['username'], parts['password'] = userinfo[0], userinfo[1]
            value = value[pos+1:]
        else:
            parts['username'], parts['password'] = None, None

        # www.example.com:80/path/to/file
        pos = value.find('/')
        if pos > -1:
            parts['path'] = value[pos:]
            value = value[:pos]
        elif self.useDefaults:
            parts['path'] = '/'
        else: 
            parts['path'] = None

        # www.example.com:80
        pos = value.find(':')
        if pos > -1:
            parts['port'] = value[pos+1:]
            value = value[:pos]
        else:
            parts['port'] = None

        # www.example.com
        if len(value) > 0:
            parts['hostname'] = value
        elif parts['path'] is None:
            raise Exception("Must provide a valid hostname or path")
        else:
            parts['hostname'] = None

        return parts

    def _get_xlds (self, value, tld=None, sld=None):
        if tld is None:
            pos = value.rfind('.')
            tld = value[pos+1:]
            value = value[:pos]
        tldSlds = self._slds[tld]
        if tldSlds is not None:
            tldSlds = tldSlds.split('|')
            pos = value.rfind('.')
            if pos > -1:
                value = value[pos+1:]
                if value in tldSlds:
                    sld = value
        return {"tld": tld, "sld": sld}

    # from https://github.com/medialize/URI.js/blob/gh-pages/src/SecondLevelDomains.js
    _slds = {
        "ac":"com|gov|mil|net|org",
        "ae":"ac|co|gov|mil|name|net|org|pro|sch",
        "af":"com|edu|gov|net|org",
        "al":"com|edu|gov|mil|net|org",
        "ao":"co|ed|gv|it|og|pb",
        "ar":"com|edu|gob|gov|int|mil|net|org|tur",
        "at":"ac|co|gv|or",
        "au":"asn|com|csiro|edu|gov|id|net|org",
        "ba":"co|com|edu|gov|mil|net|org|rs|unbi|unmo|unsa|untz|unze",
        "bb":"biz|co|com|edu|gov|info|net|org|store|tv",
        "bh":"biz|cc|com|edu|gov|info|net|org",
        "bn":"com|edu|gov|net|org",
        "bo":"com|edu|gob|gov|int|mil|net|org|tv",
        "br":"adm|adv|agr|am|arq|art|ato|b|bio|blog|bmd|cim|cng|cnt|com|coop|ecn|edu|eng|esp|etc|eti|far|flog|fm|fnd|fot|fst|g12|ggf|gov|imb|ind|inf|jor|jus|lel|mat|med|mil|mus|net|nom|not|ntr|odo|org|ppg|pro|psc|psi|qsl|rec|slg|srv|tmp|trd|tur|tv|vet|vlog|wiki|zlg",
        "bs":"com|edu|gov|net|org",
        "bz":"du|et|om|ov|rg",
        "ca":"ab|bc|mb|nb|nf|nl|ns|nt|nu|on|pe|qc|sk|yk",
        "ck":"biz|co|edu|gen|gov|info|net|org",
        "cn":"ac|ah|bj|com|cq|edu|fj|gd|gov|gs|gx|gz|ha|hb|he|hi|hl|hn|jl|js|jx|ln|mil|net|nm|nx|org|qh|sc|sd|sh|sn|sx|tj|tw|xj|xz|yn|zj",
        "co":"com|edu|gov|mil|net|nom|org",
        "cr":"ac|c|co|ed|fi|go|or|sa",
        "cy":"ac|biz|com|ekloges|gov|ltd|name|net|org|parliament|press|pro|tm",
        "do":"art|com|edu|gob|gov|mil|net|org|sld|web",
        "dz":"art|asso|com|edu|gov|net|org|pol",
        "ec":"com|edu|fin|gov|info|med|mil|net|org|pro",
        "eg":"com|edu|eun|gov|mil|name|net|org|sci",
        "er":"com|edu|gov|ind|mil|net|org|rochest|w",
        "es":"com|edu|gob|nom|org",
        "et":"biz|com|edu|gov|info|name|net|org",
        "fj":"ac|biz|com|info|mil|name|net|org|pro",
        "fk":"ac|co|gov|net|nom|org",
        "fr":"asso|com|f|gouv|nom|prd|presse|tm",
        "gg":"co|net|org",
        "gh":"com|edu|gov|mil|org",
        "gn":"ac|com|gov|net|org",
        "gr":"com|edu|gov|mil|net|org",
        "gt":"com|edu|gob|ind|mil|net|org",
        "gu":"com|edu|gov|net|org",
        "hk":"com|edu|gov|idv|net|org",
        "id":"ac|co|go|mil|net|or|sch|web",
        "il":"ac|co|gov|idf|k12|muni|net|org",
        "in":"ac|co|edu|ernet|firm|gen|gov|i|ind|mil|net|nic|org|res",
        "iq":"com|edu|gov|i|mil|net|org",
        "ir":"ac|co|dnssec|gov|i|id|net|org|sch",
        "it":"edu|gov",
        "je":"co|net|org",
        "jo":"com|edu|gov|mil|name|net|org|sch",
        "jp":"ac|ad|co|ed|go|gr|lg|ne|or",
        "ke":"ac|co|go|info|me|mobi|ne|or|sc",
        "kh":"com|edu|gov|mil|net|org|per",
        "ki":"biz|com|de|edu|gov|info|mob|net|org|tel",
        "km":"asso|com|coop|edu|gouv|k|medecin|mil|nom|notaires|pharmaciens|presse|tm|veterinaire",
        "kn":"edu|gov|net|org",
        "kr":"ac|busan|chungbuk|chungnam|co|daegu|daejeon|es|gangwon|go|gwangju|gyeongbuk|gyeonggi|gyeongnam|hs|incheon|jeju|jeonbuk|jeonnam|k|kg|mil|ms|ne|or|pe|re|sc|seoul|ulsan",
        "kw":"com|edu|gov|net|org",
        "ky":"com|edu|gov|net|org",
        "kz":"com|edu|gov|mil|net|org",
        "lb":"com|edu|gov|net|org",
        "lk":"assn|com|edu|gov|grp|hotel|int|ltd|net|ngo|org|sch|soc|web",
        "lr":"com|edu|gov|net|org",
        "lv":"asn|com|conf|edu|gov|id|mil|net|org",
        "ly":"com|edu|gov|id|med|net|org|plc|sch",
        "ma":"ac|co|gov|m|net|org|press",
        "mc":"asso|tm",
        "me":"ac|co|edu|gov|its|net|org|priv",
        "mg":"com|edu|gov|mil|nom|org|prd|tm",
        "mk":"com|edu|gov|inf|name|net|org|pro",
        "ml":"com|edu|gov|net|org|presse",
        "mn":"edu|gov|org",
        "mo":"com|edu|gov|net|org",
        "mt":"com|edu|gov|net|org",
        "mv":"aero|biz|com|coop|edu|gov|info|int|mil|museum|name|net|org|pro",
        "mw":"ac|co|com|coop|edu|gov|int|museum|net|org",
        "mx":"com|edu|gob|net|org",
        "my":"com|edu|gov|mil|name|net|org|sch",
        "nf":"arts|com|firm|info|net|other|per|rec|store|web",
        "ng":"biz|com|edu|gov|mil|mobi|name|net|org|sch",
        "ni":"ac|co|com|edu|gob|mil|net|nom|org",
        "np":"com|edu|gov|mil|net|org",
        "nr":"biz|com|edu|gov|info|net|org",
        "om":"ac|biz|co|com|edu|gov|med|mil|museum|net|org|pro|sch",
        "pe":"com|edu|gob|mil|net|nom|org|sld",
        "ph":"com|edu|gov|i|mil|net|ngo|org",
        "pk":"biz|com|edu|fam|gob|gok|gon|gop|gos|gov|net|org|web",
        "pl":"art|bialystok|biz|com|edu|gda|gdansk|gorzow|gov|info|katowice|krakow|lodz|lublin|mil|net|ngo|olsztyn|org|poznan|pwr|radom|slupsk|szczecin|torun|warszawa|waw|wroc|wroclaw|zgora",
        "pr":"ac|biz|com|edu|est|gov|info|isla|name|net|org|pro|prof",
        "ps":"com|edu|gov|net|org|plo|sec",
        "pw":"belau|co|ed|go|ne|or",
        "ro":"arts|com|firm|info|nom|nt|org|rec|store|tm|www",
        "rs":"ac|co|edu|gov|in|org",
        "sb":"com|edu|gov|net|org",
        "sc":"com|edu|gov|net|org",
        "sh":"co|com|edu|gov|net|nom|org",
        "sl":"com|edu|gov|net|org",
        "st":"co|com|consulado|edu|embaixada|gov|mil|net|org|principe|saotome|store",
        "sv":"com|edu|gob|org|red",
        "sz":"ac|co|org",
        "tr":"av|bbs|bel|biz|com|dr|edu|gen|gov|info|k12|name|net|org|pol|tel|tsk|tv|web",
        "tt":"aero|biz|cat|co|com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|travel",
        "tw":"club|com|ebiz|edu|game|gov|idv|mil|net|org",
        "mu":"ac|co|com|gov|net|or|org",
        "mz":"ac|co|edu|gov|org",
        "na":"co|com",
        "nz":"ac|co|cri|geek|gen|govt|health|iwi|maori|mil|net|org|parliament|school",
        "pa":"abo|ac|com|edu|gob|ing|med|net|nom|org|sld",
        "pt":"com|edu|gov|int|net|nome|org|publ",
        "py":"com|edu|gov|mil|net|org",
        "qa":"com|edu|gov|mil|net|org",
        "re":"asso|com|nom",
        "ru":"ac|adygeya|altai|amur|arkhangelsk|astrakhan|bashkiria|belgorod|bir|bryansk|buryatia|cbg|chel|chelyabinsk|chita|chukotka|chuvashia|com|dagestan|e-burg|edu|gov|grozny|int|irkutsk|ivanovo|izhevsk|jar|joshkar-ola|kalmykia|kaluga|kamchatka|karelia|kazan|kchr|kemerovo|khabarovsk|khakassia|khv|kirov|koenig|komi|kostroma|kranoyarsk|kuban|kurgan|kursk|lipetsk|magadan|mari|mari-el|marine|mil|mordovia|mosreg|msk|murmansk|nalchik|net|nnov|nov|novosibirsk|nsk|omsk|orenburg|org|oryol|penza|perm|pp|pskov|ptz|rnd|ryazan|sakhalin|samara|saratov|simbirsk|smolensk|spb|stavropol|stv|surgut|tambov|tatarstan|tom|tomsk|tsaritsyn|tsk|tula|tuva|tver|tyumen|udm|udmurtia|ulan-ude|vladikavkaz|vladimir|vladivostok|volgograd|vologda|voronezh|vrn|vyatka|yakutia|yamal|yekaterinburg|yuzhno-sakhalinsk",
        "rw":"ac|co|com|edu|gouv|gov|int|mil|net",
        "sa":"com|edu|gov|med|net|org|pub|sch",
        "sd":"com|edu|gov|info|med|net|org|tv",
        "se":"a|ac|b|bd|c|d|e|f|g|h|i|k|l|m|n|o|org|p|parti|pp|press|r|s|t|tm|u|w|x|y|z",
        "sg":"com|edu|gov|idn|net|org|per",
        "sn":"art|com|edu|gouv|org|perso|univ",
        "sy":"com|edu|gov|mil|net|news|org",
        "th":"ac|co|go|in|mi|net|or",
        "tj":"ac|biz|co|com|edu|go|gov|info|int|mil|name|net|nic|org|test|web",
        "tn":"agrinet|com|defense|edunet|ens|fin|gov|ind|info|intl|mincom|nat|net|org|perso|rnrt|rns|rnu|tourism",
        "tz":"ac|co|go|ne|or",
        "ua":"biz|cherkassy|chernigov|chernovtsy|ck|cn|co|com|crimea|cv|dn|dnepropetrovsk|donetsk|dp|edu|gov|if|in|ivano-frankivsk|kh|kharkov|kherson|khmelnitskiy|kiev|kirovograd|km|kr|ks|kv|lg|lugansk|lutsk|lviv|me|mk|net|nikolaev|od|odessa|org|pl|poltava|pp|rovno|rv|sebastopol|sumy|te|ternopil|uzhgorod|vinnica|vn|zaporizhzhe|zhitomir|zp|zt",
        "ug":"ac|co|go|ne|or|org|sc",
        "uk":"ac|bl|british-library|co|cym|gov|govt|icnet|jet|lea|ltd|me|mil|mod|national-library-scotland|nel|net|nhs|nic|nls|org|orgn|parliament|plc|police|sch|scot|soc",
        "us":"dni|fed|isa|kids|nsn",
        "uy":"com|edu|gub|mil|net|org",
        "ve":"co|com|edu|gob|info|mil|net|org|web",
        "vi":"co|com|k12|net|org",
        "vn":"ac|biz|com|edu|gov|health|info|int|name|net|org|pro",
        "ye":"co|com|gov|ltd|me|net|org|plc",
        "yu":"ac|co|edu|gov|org",
        "za":"ac|agric|alt|bourse|city|co|cybernet|db|edu|gov|grondar|iaccess|imt|inca|landesign|law|mil|net|ngo|nis|nom|olivetti|org|pix|school|tm|web",
        "zm":"ac|co|com|edu|gov|net|org|sch"
    }
