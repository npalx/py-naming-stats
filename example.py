import function_names_statistic
import site

projects = [
    'flask',
    'pyramid',
    'requests',
    'sqlalchemy',
]

root_path = site.getsitepackages()[0]  # '/usr/lib/python3.7/site-packages'
counted_verbs = function_names_statistic.get_top_verbs_in_multiple_projects(root_path, projects, 5)
for verb, count in counted_verbs:
    print(verb, count)
