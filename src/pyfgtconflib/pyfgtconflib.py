from collections import defaultdict
from functools import reduce

f = lambda: defaultdict(f)

def getFromDict(dataDict, mapList):
    return reduce(lambda d, k: d[k], mapList, dataDict)

def setInDict(dataDict, mapList, value):
    getFromDict(dataDict, mapList[:-1])[mapList[-1]] = value

class Parser(object):
    previous_set_headers = {}
    previous_set_values = {}

    def __init__(self):
        self.config_header = []
        self.section_dict = defaultdict(f)

	# parse "config"
    def parse_config(self, fields):
        self.config_header.append(' '.join(fields))

	# parse "edit"
    def parse_edit(self, line):
        self.config_header.append(' '.join(line))

	# parse "set" (key/value)
    def parse_set(self, line):
        values = []
        key = ' '.join([line[0], line[1]])
        values.append(' '.join(line[2:]))
        self.previous_set_values = values
        headers= self.config_header + [key]
        self.previous_set_headers = headers
        setInDict(self.section_dict, headers, values)

	# parse "set" (key/multiline value)
    def parse_set_multiline(self, line):
        self.previous_set_values.append(' '.join(line[0:]))
        setInDict(self.section_dict, self.previous_set_headers, self.previous_set_values)

	# parse "unset" (key/no value)
    def parse_unset(self, line):
        key = ' '.join([line[0], line[1]])
        values = ' '.join(line[2:])
        headers= self.config_header + [key]
        self.previous_set_headers = headers
        setInDict(self.section_dict, headers, values)

	# parse "next" (for "config" or "edit")
    def parse_next(self, line):
        if not (set(self.config_header)).issubset(set(self.previous_set_headers)):
            if self.previous_set_headers == {} and self.config_header[0] == 'config vdom':
                getFromDict(self.section_dict, ['config global'])
            getFromDict(self.section_dict, self.config_header)
        self.config_header.pop()

    # parse "end" (for "config" or "edit")
	# in multi vdom configuration, config vdom -> edit vdom_name -> end, without a next, which we need to handle it...
    def parse_end(self, line):
        if not (set(self.config_header)).issubset(set(self.previous_set_headers)):
            getFromDict(self.section_dict, self.config_header)
        if (set(self.config_header)).issubset(set(self.previous_set_headers)) and len(self.config_header) == 2 and self.config_header[0] == 'config vdom':
            self.config_header.pop()    # we need this 2nd pop to close the config vdom wihout next properly
        self.config_header.pop()

	# prase FortiGate configuration
    def parse_text(self, text):
        gen_lines = (line.rstrip() for line in text if line.strip())
        previous_method = None
        for line in gen_lines:
            fields = line.strip().split(' ')

            valid_fields= ['config', 'edit', 'set', 'unset', 'next', 'end']
            if fields[0] in valid_fields:
                method = fields[0]
                previous_method = method
                # call parse function according to the verb
                getattr(Parser, 'parse_' + method)(self, fields)
            elif previous_method == 'set':  # parse multiline value in set
                getattr(Parser, 'parse_' + 'set_multiline')(self, fields)
            elif line.startswith('#'):      # parse comment line (configuration headers)
                getFromDict(self.section_dict, [line])

        return self.section_dict