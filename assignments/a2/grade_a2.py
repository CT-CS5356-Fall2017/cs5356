from __future__ import print_function
import random
import string
import json, sys
try:
    import requests
except ImportError:
    print("It seems like you don't have 'requests' library.\n"
          "Install it using pip (https://pip.pypa.io/en/stable/installing/).\n"
          "$ pip install requests\n\n"
          "And then rerun this file. $ python grade_a2.py <url>")
    exit(-1)


def random_tag(n=4):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) 
                   for _ in range(4))


if len(sys.argv)<2 or not sys.argv[1].startswith('http'):
    print("Expect a url as an argument. Please run as follows:\n"
          "$ python {} <your-url>\n".format(sys.argv[0])
          )
    exit(-1)

URL = sys.argv[1]

def get_receipts():
    url = URL + '/receipts'
    r = requests.get(url)
    if not r.ok:
        print("ERROR: Failed while GETting {}".format(url))
        return -1
    return r.json()

def post_receipts(num=1):
    url = URL + '/receipts'
    d = {'merchant': 'M' + str(num), "amount": num}
    r = requests.post(url, json=d)
    if not r.ok:
        print("ERROR: Failed while POSTing {} with json={!r}".format(url, d))
        return -1
    rid = r.text
    return rid


def put_tags(rid, tag):
    url = URL + "/tags/{}".format(tag)
    d = rid
    r = requests.put(url, json=d)
    if not r.ok:
        print("Failed while PUTting {} with json={!r}".format(url, d))
        return -1
    return 0


def get_receipts_by_tag(tag):
    url = URL + "/tags/{}".format(tag)
    r = requests.get(url)
    if not r.ok:
        print("ERROR: Failed while GETting {}".format(url))
        return -1
    return r.json()


def test_netid():
    url = URL + "/netid"
    print("-"*80)
    print(">>> Testing: 'GET /netid'")
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print("ERROR: It seems the server down. Check in your browser if the\n"
              "url ({}) is working".format(url))
        exit(-1)
    if not r.ok:
        print("ERROR: Failed while GETting {}".format(url))
        return -1
    print("NetId found: {}".format(r.text))
    return 0



def test_tag_association():
    print("-"*80)
    print(">>> Testing: Tag_Association (post + put + get)")
    # Post three receipts
    rids = [int(post_receipts()) for i in range(3)]
    test_get_receipts()

    # Randomly generate two tags
    tags = [random_tag() for i in range(2)]

    a = list(range(3))
    random.shuffle(a)
    tag_assoc = {
        # add one tag to two of the receipts
        tags[0]: [rids[a[0]], rids[a[1]]],
        
        # add another tag to remaining receipt
        tags[1]: [rids[a[2]]]
    }

    # PUT the tags accordingly
    for t, _rids in tag_assoc.items():
        for _rid in _rids:
            put_tags(_rid, t)

    # Fetch the receitps based on each tag, and verify the association
    for t, _rids in tag_assoc.items():
        _rids.sort()
        r = get_receipts_by_tag(t)
        if r == -1:
            print("ERROR: Get receipts for tag ({}) failed. Stopping!"
                  "Probably there are other erros above.".format(t))
            return -1
        rid_tag = sorted([int(t['id']) for t in r])
        if rid_tag != _rids:
            print("ERROR: Returned receipts for tag={} is incorrect.\n"
                  "Expected: {}\n"
                  "Found: {}".format(t, _rids, rid_tag))
            return -1
    print("Test: Tag_Association passed successfully.")
    return 0

def test_get_receipts():
    print("-"*80)
    print(">>> Testing: GET /receipts")
    r = get_receipts()
    json.dump(r, sys.stderr, indent=2, sort_keys=True)


if __name__ == "__main__":
    r = test_netid()
    if r==0:
        r = test_tag_association()
    if r==0:
        print("\nGreat everything worked!")
