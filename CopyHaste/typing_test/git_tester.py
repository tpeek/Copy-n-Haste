# ahhhhhhhhhh
import urllib2
import re
import json
from random import randint


def get_code(language):
    # Get the 100 most recently updated repos that are large and pick one randomly.
    url = ('https://api.github.com/search/repositories?q=language:' +
           '{}+sort:updated+size:>20000&per_page=100'.format(language))
    data = json.load(urllib2.urlopen(url))
    info = data['items'][randint(0, 99)]
    repo = info['name']
    user = info['owner']['login']
    full_name = info['full_name']

    # Get the files and pick one randomly.
    repo_url = ('https://api.github.com/search/code?q=language:' +
                '{}+sort:size+repo:{}'.format(language, full_name))
    data = json.load(urllib2.urlopen(repo_url))
    path = data['items'][randint(0, len(data['items'])-1)]['path']

    # Get the raw text of the file.
    code = urllib2.urlopen("https://raw.githubusercontent.com/{}/{}/master/{}"
                           .format(user, repo, path)).read()

    # Get rid of doc strings, comments, import statements and multiple newlines.
    print code
    print '_____________________________________________________________'
    code = re.sub(r'[\s]*"{3}([\s\S]*?"{3})', '', code)
    code = re.sub(r"[\s]*'{3}([\s\S]*?'{3})", '', code)
    code = re.sub(r'[\s]*#([\w\W\s].*)', '', code)
    code = re.sub(r'[\s]*from([\w\W\s].*)', '', code)
    code = re.sub(r'[\s]*import([\w\W\s].*)', '', code)
    code = re.sub(r'^[\s]*$', '', code)
    code = re.sub(r'\n{2,}', '\n', code)
    code = re.sub(r'[ ]{4}', '\t', code)
    code = code.lstrip()
    return code


open('damn.txt', 'w').write(get_code('python'))
