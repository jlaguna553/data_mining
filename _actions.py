# author:      Javier Laguna
# propose:     make generic actions to manipulate data
#------------------------------------------------------------

from _lib import * #import libraries to use

__absolutepath__ = os.path.abspath(os.getcwd()) #get absolute path
'''
Now we complete the dir with respective OS
'''
if os.name == 'nt':
    d = '\\'
else:
    d = '/'


def f_get_json(data='', debug=False):
    r = __absolutepath__+d+data

    try:
        with open(r) as data_file:
            _data = json.load(data_file)
        if debug:
            print('The absolute path to open json is: %s' % _data)
    except Exception as e:
        print('Error loading json: %s' % e)
    return _data


def f_get_file_list(dir, debug=False):
    r = __absolutepath__ + d + dir  # make the complete route
    if debug:
        print('The absolute path to open json is: %s' % r)
    return [arch for arch in os.listdir(r) if isfile(join(r, arch))]
