import os
import re

def get_official_projects():
    official_projects = []
    for dir in os.listdir('/home/ducnv/Github/CNCF'):
        official_projects.append(dir)

    official_projects.sort()
    return official_projects


def get_projects_pushed():
    with open("list-project-pushed") as f:
        projects_pushed = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    projects_pushed = [x.strip() for x in projects_pushed]

    return projects_pushed


def absolute_file_paths(path):
    absolute_files = list()

    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            absolute_files.append(os.path.abspath(os.path.join(dirpath, f)))

    return absolute_files


def read_file_and_compare(path):
    urls = []
    if os.path.isfile(path) == True:
        with open(path, 'r') as infile:
            for line in infile:
                if "https://" in line:
                    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
                    # urls.append(extract_link_form_text(line))
                    for i in range(len(urls)):
                        print (urls[i])
                    continue
    return urls

# def extract_link_form_text(text):
#     urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
#     if len(urls) == 0:



if __name__ == '__main__':

    # path = '/home/ducnv/fujitsu-contribute/puppet-openstack_extras'

    for project in get_official_projects():
        if project not in get_projects_pushed():
            print "\n++++++++++++++++++++++++++++"
            print "++++++++++++++++++++++++++++"
            print project
            path = '/home/ducnv//Github/CNCF/' + project

            for path_file in absolute_file_paths(path):
                read_file_and_compare(path_file)




