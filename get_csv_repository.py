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


def write_csv(nome_repo, url, version, last_tag,wr):
  repo = []
  repo.append(nome_repo)
  repo.append(url)
  repo.append(version)
  repo.append(last_tag)
  wr.writerow(repo) 

def check_version(content: List[str]):
  inside= False
  for row in content.split("\n"):
    if inside  and re.search("\s*version\s*=\s*\"(.*\d.*)\"$", row):
       match=  re.search("(\s*version\s*=\s*)\"(.*\d.*)\"$", row)
       return match.group(2)
    elif re.search("\s*azurerm\s*", row):
       inside= True
  return ""    

def main(url_, token_):
  file_csv = open('repo_file.csv', 'w')
  writer = csv.writer(file_csv)
  write_csv("NOME_REPO","URL","VERSION","LAST_TAG",writer)
  gl = gitlab.Gitlab(url=url_, private_token= token_)


  group = gl.groups.get(3104)
  projects= group.projects.list(all=True,include_subgroups = True)
  
  for project in projects:
    empty=False
    prj = gl.projects.get(id=project.id)
    
    try:
      f= prj.files.get(file_path='terraform.tf', ref='master')
    except gitlab.exceptions.GitlabGetError:
      empty=True
    
    if empty == False:
      content = base64.b64decode(f.content).decode("utf-8")
    else:
      content= ""
    
    tags = prj.tags.list()
    version=check_version(content)
    
    if len(tags)> 0: 
       tag=tags[0].attributes['name']
    else:
      tag="notag" 
    write_csv(project.attributes['name'],project.attributes['http_url_to_repo'], version , tag, writer) 


  file_csv.close()



if __name__ == '__main__':
    url= sys.argv[1]
    token=  sys.argv[2]
    main(url,token)
