import gitlab.v4.objects
import csv
import sys

def write_csv(wr,repo):
    wr.writerow(repo)

def get_id(h,name):
    for i in range(len(h)):
        if h[i] == name:
            return i

def main(url_, token_):
    gl = gitlab.Gitlab(url=url_, private_token=token_)

    file_csv = open('utente_abilitate.csv', 'w', newline="")
    writer = csv.writer(file_csv)
    repo = []
    repo.append("GROUP_NAME")
    repo.append("RISORSA")
    repo.append("ACCESS_LEV")
    repo.append("DATA_RILASCIO")

    groups = gl.groups.list(get_all=True, include_subgroups=True)

    write_csv(writer, repo)

    for group in groups:
        repo = []
        name_group = group.attributes['full_name']
        repo.append(name_group)
        members = group.members_all.list(get_all=True)
        for m in members:
            resources = []
            name_member = m.attributes['name']
            create_at = m.attributes['created_at']
            if m.attributes['access_level'] == 30:
                access_level = "DEVELOPER"
            elif m.attributes['access_level'] == 40:
                access_level = "MAINTAINER"
            elif m.attributes['access_level'] == 10:
                access_level = "GUEST"
            elif m.attributes['access_level'] == 20:
                access_level = "REPORTER"
            else:
                access_level = "OWNER"

            resources.extend(repo)
            resources.append(name_member)
            resources.append(access_level)
            resources.append(create_at)
            write_csv(writer, resources)
    file_csv.close()



if __name__ == '__main__':
    url = sys.argv[1]
    token = sys.argv[2]
    main(url, token)
