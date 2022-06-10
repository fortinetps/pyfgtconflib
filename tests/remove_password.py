from pyfgtconflib import Parser

empty_str = ''
def niceprint_without_password(d, offset = 0, indent = 4):
    if d.get('config global') and d.get('config vdom'):
        for k, v in d.items():
            if v == {}:
                print (k)
        print ('')
        print ('config vdom')
        for k, _ in d['config vdom'].items():
            print (k)
            print ('next')
        print ('end')

        print ('')
        print ('config global')
        niceprint_without_password(d['config global'])
        print ('end')

        for k, v in d['config vdom'].items():
            print ('')
            print ('config vdom')
            print (k)
            niceprint_without_password(v)
            print ('end')
    else:
        for k, v in d.items():
            if isinstance(v, dict): # sub-section
                fields = k.strip().split(' ')
                method = fields[0]
                print ('{0}{1}'.format(empty_str.rjust(offset), ' '.join(fields)))  # print sub-section header
                niceprint_without_password(v, offset + indent)   # print sub-section
                if method == 'config':
                    print (empty_str.rjust(offset) + 'end')     # print sub-section footer
                elif method == 'edit':
                    print (empty_str.rjust(offset) + 'next')    # print sub-section footer
            else:                   # leaf
                if k == '':
                    return
                if k in ['set password', 'set private-key', 'set certificate']:
                    print (k + ' ********')
                    continue
                fields = k.strip().split(' ')
                if len(v):
                    print ('{0}{1} {2}'.format(empty_str.rjust(offset), ' '.join(fields), v[0]))    # print value
                    for xx in range(1, len(v)):     # print multiline value if exists
                        print (v[xx] + '\r')
                else:
                    print ('{0}{1}'.format(empty_str.rjust(offset), ' '.join(fields)))  # print unset without value

def parse_file(path):
	with open(path) as f:
		conf = Parser()
		conf.parse_text(f)
		return conf.section_dict

config = parse_file('tests/device_FG3601E_factory_default_settings.txt')
niceprint_without_password(config)