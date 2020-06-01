import configparser as cfg

class inifile():

    parser = cfg.ConfigParser()
    validBool = {'1': bool(1), 
                 'true': bool(1),
                 'yes': bool(1),
                 '0': bool(0), 
                 'false': bool(0),
                 'no': bool(0)
                 }
    
    def __init__(self, iniFilePath):
        self.iniFilePath = iniFilePath
        
    # string type
    def getString(self, section: str, key: str, default: str = '') -> str:
        """

        :rtype: str
        """
        # refresh parser content
        self.parser.read(self.iniFilePath)
        # 
        return self.parser[section][key]
    
    def writeString(self, section: str, key: str, value: str):
        # refresh parser content
        self.parser.read(self.iniFilePath)
        # update key
        self.parser[section][key] = value
        # persist to file
        with open(self.iniFilePath, 'w') as iniFile:
          self.parser.write(iniFile)
        
    # number type
    def getLong(self, section: str, key: str, default = 0) -> int:
        val = self.getString(section, key)
        if val.isnumeric():
            return int(val)
        
        return int(default)
    
    def writeLong(self, section: str, key: str, value: int):
        stringVal = f'{value}'
        self.writeString(section, key, stringVal)

    # double type
    def getDouble(self, section: str, key: str, default = 0.0) -> float:
        return float(self.getString(section, key))
    
    def writeDouble(self, section, key, value):
        stringVal = f'{value}'
        self.writeString(section, key, stringVal)
    
    # Boolean type    
    def getBool(self, section: str, key: str, default = True) -> bool:
        val = self.getString(section, key)
        
        if val in self.validBool:
            return self.validBool[val]
            
        return default
    
    def writeBool(self, section: str, key: str, value: bool):
        pass       

# test code
if __name__ == "__main__":
    configIni = inifile('d:/testconfig/config.ini')
    
    address = configIni.getString('Settings', 'ip address', '127.0.0.1')
    port = configIni.getLong('Settings', 'Port')
    
    configIni.writeLong('Settings', 'Port', 801)  
    
    crlf = configIni.getBool('Settings', 'CRLF', False)