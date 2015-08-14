@csrf_exempt
def get_content_view2(request):
    user = request.POST['user']
    repo = request.POST['repo']
    path = request.POST['path']
    code = urllib.urlopen("https://raw.githubusercontent.com/{}/{}/master/{}"
                          .format(user, repo, path)).read()
    code = str(code)
    # import pdb; pdb.set_trace()
    # code = re.sub(r'"""([\w\W\s]+)"""', '', code)
    code = re.sub(r'#([\w\W\s].*)', '', code)
    code = re.sub(r'from([\w\W\s].*)', '', code)
    code = re.sub(r'import([\w\W\s].*)', '', code)

    return HttpResponse(code)
