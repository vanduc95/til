import yaml

with open("confluence.yml", 'r') as stream:
    try:
        # print(yaml.load(stream))
        a = yaml.load(stream)
        print(a['confluence']['email'])
    except yaml.YAMLError as exc:
        print(exc)


a = {'confluence': {'email': 'ducnguyenvan.bk@gmail.com', 'token': 'FuQ3CPOPixm5VEaON7CV2BB8',
                    'space_key': 'ACB123', 'root_url': 'https://toavnhieu.atlassian.net',
                    'title': 'Azure Virtual Machine1'}}

print(a['confluence'])