import json
import os

file_pathDB = '../db/subreddittest.json'


def createJSONBD(file_path):
    # verify if file exist
    if os.path.isfile(file_path):
        print("File Exist")
    else:
        with open(file_path, 'w') as f:
            f.write('{"exist": [],"subreddit": {}}')
            f.close()
        print("File created")


def whatIsBeforeId(subreddit, file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        for sub in data["exist"]:
            if sub == subreddit:
                before_id = data['subreddit'][subreddit]['before_id']
                return before_id
            else:
                return None


def addBeforeId(subreddit, before_id, file_path):
    with open(file_path, 'r') as f:
        data = json.loads(f.read())
        if subreddit in data['exist']:
            data['subreddit'][subreddit]['before_id'] = before_id
            with open(file_path, 'w') as fe:
                json.dump(data, fe, indent=3)
            return "Before ID Updated"
        else:
            data['exist'].append(subreddit)
            data['subreddit'][subreddit] = {'before_id': before_id}
            with open(file_path, 'w') as fw:
                json.dump(data, fw, indent=3)
            return "New Subreddit Added"

if __name__ == '__main__':
    print(whatIsBeforeId('test', file_pathDB))
    print(addBeforeId('test', 'ok', file_pathDB))
    print(whatIsBeforeId('test', file_pathDB))