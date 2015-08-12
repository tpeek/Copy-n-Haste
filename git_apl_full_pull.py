import github3

repo = github3.repository('heyiamjames', 'CodingInterviewPractice')
contents = repo.file_contents('/close_far.py')

print(contents.name)
print(contents.decoded)


repo = github3.repository({0}, {1}).format('heyiamjames', 'CodingInterviewPractice')
contents = repo.file_contents('/close_far.py')

print(contents.decoded)

s1 = " {0} is better than {1} ".format("emacs", "vim")
