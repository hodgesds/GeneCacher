try:
    import pylibmc as memcache
except:
    import memcache
import hashlib as h


class tools:
    def __init__(self, 
            cache_prefix=None, 
            cache_servers=['127.0.0.1:11211'], 
            cache_timeout=0 # 0 is default to keep in cache...
        ):
        self.cache_prefix = cache_prefix or ''
        self.servers = cache_servers
        self.client = memcache.Client(self.servers)
        self.cache_timeout = cache_timeout

    def hasher(self, chrome, pos):
        #a = h.sha256()
        #a.update(chrome+':'+str(pos))
        #return self.cache_prefix+a.hexdigest()
        return chrome + ':' + str(pos)
        
    def cache_fasta(self, fasta, startbp=1, insert_size=1000000):
        chrome = ''
        pos = startbp
        with open(fasta) as f:
            out = {}
            for row in f:
                # turn this into a function...
                if '>' in row:
                    # insert any stragglers
                    self.client.set_multi(out, time=self.cache_timeout, key_prefix=self.cache_prefix)
                    chrome = row.replace('\n','').replace('>','')
                    pos = startbp
                    out = {}
                    print 'Working on chromosome',chrome
                else:
                    data = row.replace('\n','')
                    for value in data:
                        key = self.hasher(chrome, pos)
                        out[key] = value
                        pos += 1
                        if len(out) == insert_size:
                            self.client.set_multi(out, time=self.cache_timeout, key_prefix=self.cache_prefix)   
                            out = {}
            # last chance
            self.client.set_multi(out, time=self.cache_timeout, key_prefix=self.cache_prefix)   
    
    def get_base(self, chrome, pos):
        return self.client.get(self.hasher(chrome,pos))    
    
    def get_region(self, region):
        ''' grabs a region in chrX:1-100 format '''
        chrome = region.split(':')[0]
        lower = int(region.split(':')[1].split('-')[0])
        upper = int(region.split(':')[1].split('-')[1])
        keys = [ chrome+':'+str(i) for i in range(lower,upper+1)]
        return self.client.get_multi(keys, key_prefix=self.cache_prefix)
        
    def clear_cache(self):
        return self.client.flush_all()

