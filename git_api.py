
GET /repos/:owner/:repo/contents/:path

Status: 200 OK
X-RateLimit-Limit: 5000
X-RateLimit-Remaining: 4999
{
  "type": "file",
  "encoding": "base64",
  "size": 5362,
  "name": "README.md",
  "path": "README.md",
  "content": "encoded content ...",
  "sha": "3d21ec53a331a6f037a91c368710b99387d012c1",
  "url": "https://api.github.com/repos/octokit/octokit.rb/contents/README.md",
  "git_url": "https://api.github.com/repos/octokit/octokit.rb/git/blobs/3d21ec53a331a6f037a91c368710b99387d012c1",
  "html_url": "https://github.com/octokit/octokit.rb/blob/master/README.md",
  "download_url": "https://raw.githubusercontent.com/octokit/octokit.rb/master/README.md",
  "_links": {
    "git": "https://api.github.com/repos/octokit/octokit.rb/git/blobs/3d21ec53a331a6f037a91c368710b99387d012c1",
    "self": "https://api.github.com/repos/octokit/octokit.rb/contents/README.md",
    "html": "https://github.com/octokit/octokit.rb/blob/master/README.md"
  }
}


#do this before
# Get the SHA of some branch. There must be a better way to do this.
git log -1 --pretty=oneline origin/somebranch | sed -E "s/^([^[:space:]]+).*/\1/"

to find the ssh of a gist, clone it and look a commit Key 
git log

#steps
in term by proj > curl -i https://api.github.com/users/octocat/orgs


HTTP/1.1 200 OK
Server: GitHub.com
Date: Mon, 10 Aug 2015 17:19:14 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 5
Status: 200 OK
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1439230754
Cache-Control: public, max-age=60, s-maxage=60
ETag: "98f0c1b396a4e5d54f4d5fe561d54b44"
Vary: Accept
X-GitHub-Media-Type: github.v3
X-XSS-Protection: 1; mode=block
X-Frame-Options: deny
Content-Security-Policy: default-src 'none'
Access-Control-Allow-Credentials: true
Access-Control-Expose-Headers: ETag, Link, X-GitHub-OTP, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset, X-OAuth-Scopes, X-Accepted-OAuth-Scopes, X-Poll-Interval
Access-Control-Allow-Origin: *
X-GitHub-Request-Id: C73B6BDA:44D3:19597131:55C8DD12
Strict-Transport-Security: max-age=31536000; includeSubdomains; preload
X-Content-Type-Options: nosniff
Vary: Accept-Encoding
X-Served-By: 2d7a5e35115884240089368322196939

gist id : b3f9f3bf0c4428e5bfaf
GET /gists/b3f9f3bf0c4428e5bfaf/:sha

:sha 
a9252f2a25697b5e9079b0e421a78f1773580a79

GET /gists/b3f9f3bf0c4428e5bfaf/a9252f2a25697b5e9079b0e421a78f1773580a79

>>  pip install --pre github3.py
2 dependencies:
 pip install requests
pip install uritemplate.py

--------------get all them repostories ----------

import github3
for repository in github3.all_repositories(number=50):
    print('{0}, id: {0.id}, url: {0.html_url}'.format(repository))

gh = github3.login('username', 'password')
for repository in gh.all_repositories():
    print('{0} - id: {0.id}, url: {0.html_url}'.format(repository))


--------------get them contesnts of the repository ----------
import github3
repo = github3.repository('heyiamjames', 'CodingInterviewPractice')
contents = repo.file_contents('/close_far.py')

print(contents.name)
print(contents.decoded)


....
for the contents

mine
https://github.com/HeyIamJames/CodingInterviewPractice/blob/master/close_far.py
