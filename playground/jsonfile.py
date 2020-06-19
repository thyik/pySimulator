import json

class json_file:

    def __init__(self, file):
        self.cfg_file = file
        
    def read(self):
        with open(self.cfg_file) as json_file:
            self.data = json.load(json_file)

    def write(self):
        with open(self.cfg_file, 'w') as outfile:
            json.dump(self.data, outfile)

    def valid(self, section, key):
        if section not in self.data:
            return False
        
        if key not in self.data[section]:
            return False
        
        return True
    
    def get(self, section, key):
        if not self.valid(section, key):
            return ''

        return self.data[section][key]

    def set(self, section, key, value):
        if not self.valid(section, key):
            return
            
        self.data[section][key] = value

    def get_string(self, section, key):
        if not self.valid(section, key):
            return ''
            
        return self.data[section][key]

    def get_int(self, section, key):
        if not self.valid(section, key):
            return 0
            
        return self.data[section][key]

    def print_section(self, section):
        for p in self.data[section]:
            print('IN: ' + p['in'])
            print('OUT: ' + p['out'])
            print('EOL: ' + p['eol'])
            print('')
                 
if __name__ == "__main__":
    js = json_file('config.json')
    
    js.read()
    
    js.print_section('protocol')
    
    s = js.get_string('connection', 'ServerIPAddress')
    i = js.get_int('setting', 'ClientPort')
   
    js.set('setting', 'ClientPort', 800)
    js.set('settings', 'Port', 801)
    print(s)
    print(i)
    
    js.write()
    
   