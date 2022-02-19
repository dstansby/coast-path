import json


def un_minify_json():
    fname = 'SW_Coast_Path_Full.json'
    with open(fname, 'r') as f:
        j = json.loads(f.read())

    with open(fname, 'w') as f:
        f.seek(0)
        json.dump(j, f, indent=' ')
        f.truncate()


if __name__ == '__main__':
    un_minify_json()
