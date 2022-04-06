import gitlab
import gitlab.v4.objects
from gitlab.base import RESTManager, RESTObject
from dataclasses import dataclass
import csv
from typing import Union, List
import base64
from gitlab.v4.objects.projects import Project
import re
import sys

def export_file(content: List[str]):
  inside= False
  for row in content.split("\n"):
    if inside  and re.search("\s*version\s*=\s*\"(.*\d.*\"$)", row):
       match=  re.search("(\s*version\s*=\s*)\"(.*\d.*\"$)", row)
       return match.group(2)
    elif re.search("\s*azurerm\s*", row):
       inside= True
    

def main(url_, token_):
  file_csv = open('repo_file', 'w')
  writer = csv.writer(file_csv)
  header = ["NOME_REPO","URL","VERSION","LAST_TAG"]
  writer.writerow(header)  
  gl = gitlab.Gitlab(url=url_, private_token= token_)


  group = gl.groups.get(3104)
#  for project in group.projects.list():
#      print(project.attributes['name'],end = ' ')
#      print(project.attributes['http_url_to_repo'])
  projects= group.projects.list(all=True,include_subgroups = True)
  for project in projects:
   # repo=["'"+project.attributes['name']+"','"+project.attributes['http_url_to_repo']+"'"]
    prj = gl.projects.get(id=project.id)

    try:
      f= prj.files.get(file_path='tests/terraform.tf', ref='master')
    except gitlab.exceptions.GitlabGetError:
      continue
    content = base64.b64decode(f.content).decode("utf-8")

    export_file(content)
    tags = prj.tags.list()
    
    repo = []
    repo.append(project.attributes['name'])
    repo.append(project.attributes['http_url_to_repo'])
    repo.append(export_file(content))




    if len(tags)> 0: 
       repo.append(tags[0].attributes['name'])
       print (tags[0].attributes['name'])
    else:
      repo.append("no tags")
    writer.writerow(repo)


    #prj = gl.projects.get(id=project.id)

   # try:
    #  f= prj.files.get(file_path='tests/terraform.tf', ref='master')
   # except gitlab.exceptions.GitlabGetError:
  #    continue
 #   content = base64.b64decode(f.content).decode("utf-8")

  file_csv.close()


if __name__ == '__main__':
    url= sys.argv[1]
    token=  sys.argv[2]
    main(url,token)
