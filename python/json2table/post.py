import sys
import os
import requests
import ast

from json2table import convert


def convert_json2table(json_input):

    build_direction = "LEFT_TO_RIGHT"
    html = convert(json_input, build_direction)
    return html


def post_to_confluence():
    string_json = sys.argv[1]

    table_html = convert_json2table(ast.literal_eval(string_json))
    headers = {
        'Content-Type': 'application/json',
    }

    data = '{"type":"page","title":"new page23","space":{"key":"RAID"},"body":{"storage":{"value":"<html>' \
           + table_html + '</html>","representation":"storage"}}}'

    response = requests.post('https://toavnhieu.atlassian.net/wiki/rest/api/content/', headers=headers, data=data,
                             auth=('tovanhieu1996.hl@gmail.com', 'ScWMZRxIg7eVVS4JeDv5121F'))

    print(response)


def write_file(string_json):
    folder = os.path.dirname(os.path.abspath(__file__))
    file_name = folder + "/table.html"
    f = open(file_name, "w")
    f.write(string_json)
    f.close()


if __name__ == '__main__':
    # string_json1 = sys.argv[1]
    post_to_confluence()