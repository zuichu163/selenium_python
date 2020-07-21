from configparser import ConfigParser

class ReadIni():
    def __init__(self, filename=None, node=None):
        if filename == None:
            filename = 'E:/www/seleniumPython/config/local_element.ini'
        self.cf = self.load_ini(filename)
        if node == None:
            self.node = 'RegisterElement'
        else:
            self.node = node

    def load_ini(self, filename):
        cf = ConfigParser()
        cf.read(filename)
        return cf

    def get_value(self, key):
        value = self.cf.get(self.node, key)
        return value