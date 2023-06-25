import json
import os

file_pathDB = '../db/subreddittest.json'


def createJSONBD(file_path):
    # verify if file exist
    if os.path.isfile(file_path):
        print("File Exist")
    else:
        with open(file_path, 'w') as f:
            f.write('{"subreddit": {}}')
            f.close()
        print("File created")


def whatIsBeforeId(subreddit, file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    if not data['subreddit'][subreddit]:
        return "No Before ID"
    else:
        before_id = data['subreddit'][subreddit]['before_id']
        return before_id



def addBeforeId(subreddit, before_id, file_path):
    with open(file_path, 'r') as f:
        data = json.loads(f.read())
        # verify if subreddit exist in the file
        if subreddit in data['subreddit']:
            data['subreddit'][subreddit]['before_id'] = before_id
            with open(file_path, 'w') as fe:
                json.dump(data, fe, indent=4)
                return "Before ID Updated"
        else:
            # add new subreddit
            data['subreddit'][subreddit] = {"before_id": before_id}
            with open(file_path, 'w') as fw:
                json.dump(data, fw, indent=4)
                return "New Subreddit Added"


if __name__ == '__main__':
    addBeforeId(subreddit='test2', before_id='gfgzf', file_path=file_pathDB)
    print(whatIsBeforeId(subreddit='test', file_path=file_pathDB))
    print(whatIsBeforeId(subreddit='test4', file_path=file_pathDB))