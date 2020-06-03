import configparser as cfg


class IniFile:

    def __init__(self, file_path):
        """constructor

        Keyword arguments:
        file_path -- ini file location
        """
        self._file_path = file_path

        # setup parser behaviour
        self._parser = cfg.ConfigParser(
            delimiters={'='},
            interpolation=None
        )
        self._parser.BOOLEAN_STATES = {
            '1': True,
            'true': True,
            'yes': True,
            '0': False,
            'false': False,
            'no': False
        }
        # load file
        self.refresh()

    def refresh(self):
        # refresh parser content
        self._parser.read(self._file_path)

    # string type
    def get_string(self, section: str, key: str, default: str = '') -> str:
        """return string value.

        Keyword arguments:
        section -- section name
        key -- key name
        default -- default value to return if section / key not found (default '')
        """
        # check section exist
        if not self._parser.has_section(section):
            return default

        # check key exist
        if not self._parser.has_option(section, key):
            return default

        return self._parser[section][key]

    def write_string(self, section: str, key: str, value: str):
        """write string value.

        Keyword arguments:
        section -- section name
        key -- key name
        value -- value to write
        """
        # update key
        self._parser[section][key] = value
        # persist to file
        with open(self._file_path, 'w') as iniFile:
            self._parser.write(iniFile)

    # number type
    def get_int(self, section: str, key: str, default=0) -> int:
        """return integer value.

        Keyword arguments:
        section -- section name
        key -- key name
        default -- default value to return if section / key not found (default 0)
        """
        val = self.get_string(section, key)
        if val.isnumeric():
            return int(val)

        return int(default)

    def write_int(self, section: str, key: str, value: int):
        """write integer value.

        Keyword arguments:
        section -- section name
        key -- key name
        value -- value to write
        """
        string_val = f'{value}'
        self.write_string(section, key, string_val)

    # double type
    def get_float(self, section: str, key: str, default=0.0) -> float:
        """return float value.

        Keyword arguments:
        section -- section name
        key -- key name
        default -- default value to return if section / key not found (default 0.0)
        """
        return float(self.get_string(section, key))

    def write_float(self, section, key, value):
        """write float value.

        Keyword arguments:
        section -- section name
        key -- key name
        value -- value to write
        """
        string_val = f'{value}'
        self.write_string(section, key, string_val)

    # Boolean type    
    def get_bool(self, section: str, key: str, default=False) -> bool:
        """return bool value.

        Keyword arguments:
        section -- section name
        key -- key name
        default -- default value to return if section / key not found (default False)
        """
        val = self.get_string(section, key)
        if val in self._parser.BOOLEAN_STATES:
            return self._parser.BOOLEAN_STATES[val]

        return default

    def write_bool(self, section: str, key: str, value: bool):
        """write bool value.

        Keyword arguments:
        section -- section name
        key -- key name
        value -- value to write
        """
        pass

    # test code


if __name__ == "__main__":
    configIni = IniFile('d:/testconfig/config.ini')

    address = configIni.get_string('Settings', 'ip address', '127.0.0.1')
    port = configIni.get_int('Settings', 'Port')

    configIni.write_int('Settings', 'Port', 801)

    crlf = configIni.get_bool('Settings', 'CRLF', False)

    print(crlf)
