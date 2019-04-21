import os
import configparser


def find_project():
    projects = []
    for dir in os.listdir('/home/ducnv/fujitsu-contribute'):
        path = "/home/ducnv/fujitsu-contribute/" + dir + "/tox.ini"
        if os.path.isfile(path) == True:
            # file = open(path, "r")
            # print file.read()

            config = configparser.ConfigParser()
            config.sections()
            config.read(path)

            if 'testenv:py27' in config and 'testenv:py36' not in config:
                projects.append(dir)

    projects.sort()
    return projects


def get_project_official():
    with open("/home/ducnv/fujitsu-contribute/project-official") as f:
        project_official = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    project_official = [x.strip() for x in project_official]

    return project_official


if __name__ == '__main__':

    with open("list-project-pushed") as f:
        project_pushed = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    list_project_pushed = [x.strip() for x in project_pushed]
    # print(list_project_pushed)

    count = 0
    for project in get_project_official():
        if project not in list_project_pushed:
            count += 1
            print(project)


