import json


def revert_dicts(dictionary):
    result = {}
    for k, v in dictionary.items():
        for elem in v:
            result.update({elem: k})
    return result


def upload_song_configs(path):
    with open(path) as f:
        song_conf = json.load(f)
    song_conf = revert_dicts(song_conf)
    return song_conf










