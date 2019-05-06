# py-naming-stats
Functions for getting naming statistics in python projects.

**get_all_words_in_project(project_path)** - Get words contained in function names in project.
**get_function_names_in_project(project_path)** - Get function names contained in python files in directory.
**get_top_function_names_in_project(project_path, limit)** - Get most common function names in project.
**get_verbs_in_project(project_path)** - Get verbs contained in the function names in project.
**get_top_verbs_in_project(project_path, limit)** - Get most common verbs contained in the function names in project.
**get_top_verbs_in_multiple_projects(root_path, projects, limit)** - Get most common verbs contained in function names in multiple projects.

### Example
```python
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
```
```python
get 384
set 183
do 132
is 117
has 92
```
