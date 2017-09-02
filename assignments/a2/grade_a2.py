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
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))


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
    url = URL + "/"
    print("-"*80)
    print(">>> Testing: 'GET /'")
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
    rids = [post_receipts() for i in range(3)]
    test_get_receipts()

    # Randomly generate two tags
    tags = [random_tag() for i in range(2)]

    # add one tag to two of the receipts
    a = list(range(3))
    random.shuffle(a)
    put_tags(rids[a[0]], tags[0])
    put_tags(rids[a[1]], tags[0])

    # add another tag to remaining receipt
    put_tags(rids[a[2]], tags[1])

    # Fetch the receitps based on each tag, and verify the association
    r = get_receipts_by_tag(tags[0])
    if r == -1:
        print("ERROR: Get receipts for tag ({}) failed. Stopping!"
              "Probably there are other erros above.".format(tags[0]))
        return -1
    rid_tag0 = [t['id'] for t in r]
    if rids[a[0]] not in rid_tag0 or rids[a[1]] not in rid_tag0:
        print("ERROR: Returned receipts for tag={} is incorrect.\n"
              "Expected: {}\n"
              "Found: {}".format(tags[0], a[:1], rid_tag0))
        return -1

    rid_tag1 = [t['id'] for t in get_receipts_by_tag(tags[1])]
    if rids[a[2]] not in rid_tag1:
        print("ERROR: Returned receipts for tag={} is incorrect.\n"
              "Expected: {}\n"
              "Found: {}".format(tags[1], a[2:], rid_tag1))
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
