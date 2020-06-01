import configparser as cfg


class IniFile:
    _parser = cfg.ConfigParser()
    _valid_bool = {'1': bool(1),
                   'true': bool(1),
                   'yes': bool(1),
                   '0': bool(0),
                   'false': bool(0),
                   'no': bool(0)
                   }

    def __init__(self, file_path):
        self._file_path = file_path

    # string type
    def get_string(self, section: str, key: str, default: str = '') -> str:
        """

        :rtype: str
        """
        # refresh parser content
        self._parser.read(self._file_path)
        # 
        return self._parser[section][key]

    def write_string(self, section: str, key: str, value: str):
        # refresh parser content
        self._parser.read(self._file_path)
        # update key
        self._parser[section][key] = value
        # persist to file
        with open(self._file_path, 'w') as iniFile:
            self._parser.write(iniFile)

    # number type
    def get_int(self, section: str, key: str, default=0) -> int:
        val = self.get_string(section, key)
        if val.isnumeric():
            return int(val)

        return int(default)

    def write_int(self, section: str, key: str, value: int):
        string_val = f'{value}'
        self.write_string(section, key, string_val)

    # double type
    def get_float(self, section: str, key: str, default=0.0) -> float:
        return float(self.get_string(section, key))

    def write_float(self, section, key, value):
        string_val = f'{value}'
        self.write_string(section, key, string_val)

    # Boolean type    
    def get_bool(self, section: str, key: str, default=True) -> bool:
        val = self.get_string(section, key)

        if val in self._valid_bool:
            return self._valid_bool[val]

        return default

    def write_bool(self, section: str, key: str, value: bool):
        pass

    # test code


if __name__ == "__main__":
    configIni = IniFile('d:/testconfig/config.ini')

    address = configIni.get_string('Settings', 'ip address', '127.0.0.1')
    port = configIni.get_int('Settings', 'Port')

    configIni.write_int('Settings', 'Port', 801)

    crlf = configIni.get_bool('Settings', 'CRLF', False)
