import re

class URL(object):
    """A class for extracting various parts of a URL"""
    def __init__ (self, value, useDefaults=False):
        self.useDefaults = useDefaults is True
        self.url = value

    def url():
        doc = "The url property."
        def fget(self):
            url = ''
            if self.protocol:
                url = self.protocol + '://'
            if self.username:
                url += self.username + ':' + self.password + '@'
            url += self.hostname
            if self.port:
                url += ':' + str(self.port)
            if self.path:
                url += self.path
            if self.query:
                url += '?' + self.query
            if self.fragment:
                url += '#' + self.fragment
            return url
        def fset(self, value):
            self._url = value
            self.__parse_url(value)
        return locals()
    url = property(**url())

    def protocol():
        doc = "The protocol property."
        def fget(self):
            return self._protocol
        def fset(self, value):
            if value is None:
                self._protocol = None
            else:
                match = re.match('[a-z][a-z0-9+-]*', value, re.I)
                if match is None:
                    raise Exception("This is not a valid protocol")
                self._protocol = value
        return locals()
    protocol = property(**protocol())

    def query():
        doc = "The query property."
        def fget(self):
            return self.__build_query()
        def fset(self, value):
            if value is None:
                self._queries = None
            else:
                self._queries = self.__parse_query(value)
        return locals()
    query = property(**query())

    def hostname():
        doc = "The hostname property."
        def fget(self):
            hostname = ''
            if self.subdomain:
                hostname += self.subdomain + '.'
            return hostname + self._domain
        def fset(self, value):
            self.__parse_hostname(value)
        return locals()
    hostname = property(**hostname())

    def domain():
        doc = "The domain property."
        def fget(self):
            return self.hostname[len(self.subdomain)+1:]
        def fset(self, value):
            self.__parse_hostname(value)
        return locals()
    domain = property(**domain())

    def __parse_hostname(self, string):
        """Extract the subdomain, domain, tld, and sld"""
        pos = string.find('.')
        if pos > -1:
            xlds = self.__get_xlds(string)
            self.tld = xlds['tld']
            self.sld = xlds['sld']
            matches = re.findall('(\.)', string)
            if len(matches) == 1 or (xlds['sld'] and len(matches) == 2):
                # example.com
                # example.co.uk
                self._domain = string
                self.subdomain = None
            else:
                # www.example.com
                # ww.example.co.uk
                pos = string.find('.')
                self._domain = string[pos+1:]
                self.subdomain = string[:pos]
        else:
            self._domain = string
            self.subdomain = None
            self.tld = None
            self.sld = None

    def __build_query(self):
        if self._queries is not None:
            return "&".join('%s=%s' % (k, v) for k,v in self._queries.iteritems())

    def __parse_query(self, string):
        queries = {}
        splitString = string.split('&')
        for query in splitString:
            pos = query.find('=')
            queries[query[:pos]] = query[pos+1:]
        return queries

    def add_query(self, query, parameter):
        self.update_query(self, query, parameter)

    def update_query(self, query, parameter):
        self._queries[query] = parameter

    def delete_query(self, query):
        self._queries.pop(query, None)

    def get_query(self, query=None):
        if query is None:
            return self.__build_query()
        return self._queries[query]

    def __parse_url(self, string):
        # http://username:password@www.example.com:80/path/to/file?query=parameter#link
        pos = string.find('#')
        if pos > -1:
            self.fragment = string[pos+1:]
            string = string[:pos]
        else:
            self.fragment = None

        # http://username:password@www.example.com:80/path/to/file?query=parameter
        pos = string.find('?')
        if pos > -1:
            self.query = string[pos+1:]
            string = string[:pos]
        else:
            self.query = None

        # http://username:password@www.example.com:80/path/to/file
        if string[0:1] == '//':
            # no scheme given
            self.protocol = None
            string = string[2:]
        else:
            pos = string.find('://')
            if pos > -1:
                self.protocol = string[:pos].lower()
                string = string[pos+3:]
            elif self.useDefaults:
                self.protocol = 'http'
            else:
                self.protocol = None

        # username:password@www.example.com:80/path/to/file
        pos = string.find('@')
        if pos > -1 and pos < string.find('/'):
            userinfo = string[:pos].split(':')
            self.username, self.password = userinfo[0], userinfo[1]
            string = string[pos+1:]
        else:
            self.username, self.password = None, None

        # www.example.com:80/path/to/file
        pos = string.find('/')
        if pos > -1:
            self.path = string[pos:]
            string = string[:pos]
        elif self.useDefaults:
            self.path = '/'
        else:
            self.path = None

        # www.example.com:80
        pos = string.find(':')
        if pos > -1:
            self.port = string[pos+1:]
            string = string[:pos]
        elif self.useDefaults and self.protocol:
            if self.protocol in self._defaultPorts:
                self.port = self._defaultPorts[self.protocol]
        else:
            self.port = None

        # www.example.com
        if len(string) > 0:
            self.hostname = string
        else:
            raise Exception("Must provide a valid hostname")

    def __get_xlds (self, string, tld=None, sld=None):
        if tld is None:
            pos = string.rfind('.')
            tld = string[pos+1:]
            string = string[:pos]
        tldSlds = self._slds.get(tld)
        if tldSlds is not None:
            tldSlds = tldSlds.split('|')
            pos = string.rfind('.')
            if pos > -1:
                string = string[pos+1:]
                if string in tldSlds:
                    sld = string
        return {"tld": tld, "sld": sld}

    _defaultPorts = {
        'ftp': '21',
        'http': '80',
        'https': '443'
    }

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