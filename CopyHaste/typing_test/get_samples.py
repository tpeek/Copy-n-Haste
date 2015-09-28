import urllib2
import re
import json
from time import sleep


def get_code(language):
    count = int(open('count.txt', 'r').read())
    # Get the 100 most recently updated large repos.
    url = ('https://api.github.com/search/repositories?q=language:' +
           language + '+sort:updated+size:>20000&per_page=100&page={}')

    repos = json.load(urllib2.urlopen(url.format(1)))
    for x in range(2, 10):
        repos['items'].extend(json.load(urllib2.urlopen(url.format(x)))['items'])

    for repo in repos['items']:
        repo_name = repo['name']
        user = repo['owner']['login']
        full_name = repo['full_name']

        repo_url = ('https://api.github.com/search/code?q=language:' +
                    '{}+sort:size+repo:{}'.format(language, full_name))
        while True:
            try:
                files = json.load(urllib2.urlopen(repo_url))
                files['items']
                break
            except:
                print 'second'
                sleep(5)

        if len(files['items']) == 0:
            continue

        for py_file in files['items']:
            path = py_file['path']
            # Get the raw text of the file.
            file_url = ("https://raw.githubusercontent.com/{}/{}/master/{}"
                        .format(user, repo_name, path))
            try:
                code = urllib2.urlopen(file_url).read()
            except:
                print 'Not Found'
                continue

            # Get rid of doc strings, comments, import statements,
            # blank lines and convert multi spaces to tabs.
            code = re.sub(r'[ ]{4}', '\t',
                re.sub(r'\n{2,}', '\n',
                re.sub(r'^[\s]*$', '',
                re.sub(r'[\s]*import([\w\W\s].*)', '',
                re.sub(r'[\s]*from([\w\W\s].*)', '',
                re.sub(r'[\s]*#([\w\W\s].*)', '',
                re.sub(r"[\s]*'{3}([\s\S]*?'{3})", '',
                re.sub(r'[\s]*"{3}([\s\S]*?"{3})', '', code)))))))).strip()

            while code[:4] == 'try:' or code[:6] == 'except':
                code = code[code.index('\n')+1:]
            if len(code) > 1200:
                open('static/samples/sample{}.txt'.format(count), 'w').write(code[:1200])
                count += 1
                if count % 10 == 0:
                    print count
                open('count.txt', 'w').write(str(count))

get_code('python')
