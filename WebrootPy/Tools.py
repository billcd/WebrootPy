import re
import json


def get_webroot_config(path_to_file):
    import yaml
    with open(path_to_file, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def camel_case_to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def snake_case_to_camel_case(name):
    new_key = ""
    for s in name.split("_"):
        new_key += s.title()
    return new_key


def urlify(obj):
    url = ""
    for key, value in obj.items():
        if value:
            url += "&" + key + "=" + value
        else:
            url += "&" + key

    if url[0] == "&":
        c = list(url)
        c[0] = "?"
        url = "".join(c)

    return url


def to_webroot_json(wr_object):
    new_wr_obj = {}
    for key, value in wr_object.__dict__.items():
        new_key = snake_case_to_camel_case(key)
        new_wr_obj[new_key] = value
    return json.dumps(new_wr_obj)


def webroot_json_to_properties(wr_object, json_data):
    for key, value in json_data.items():
        new_key = camel_case_to_snake_case(key)
        setattr(wr_object, new_key, value)
