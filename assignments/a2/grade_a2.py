from __future__ import print_function
import random
import string
import json, sys
import re
try:
    import requests
except ImportError:
    print("It seems like you don't have 'requests' library.\n"
          "Install it using pip (https://pip.pypa.io/en/stable/installing/).\n"
          "$ pip install requests\n\n"
          "And then rerun this file. $ python grade_a2.py <url>")
    exit(-1)

URL = None

def random_tag(n=4):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) 
                   for _ in range(4))


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


def test_netid(netid):
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
    if not netid:
        print("NetId found: {} (unverified)".format(r.text))
    else:
        if netid in r.text:
            print("Netid ({}) matched from the url={}!".format(netid, url))
        else:
            print("Your supplied netid={!r} not found at url={}".format(netid, url))
            return -1
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
    print("Testing tag deletion")
    for t, _rids in tag_assoc.items():
        put_tags(_rids[0], t)
    
    for t, _rids in tag_assoc.items():
        r = get_receipts_by_tag(t)
        rid_tag = [int(t['id']) for t in r]
        if _rids[0] in rid_tag:
            print("ERROR: Returned receipts for tag={} is incorrect.\n"
                  "Expected: {}\n"
                  "Found: {}".format(t, _rids[1:], rid_tag))
            return -1
    print("Test: Tag deletion also worked!! Hurray!")

    return 0


def test_get_receipts():
    print("-"*80)
    print(">>> Testing: GET /receipts")
    r = get_receipts()
    json.dump(r, sys.stderr, indent=2, sort_keys=True)


def extract_netid_and_url(line):
    regex = r'\* \[.*\]\(.*\) - (?P<netid>\w+) \- \[.+\]\((?P<url>http.+)\)\s*\[\!\[CircleCI\]\((?P<circleurl>.*)\)\]\(.*\)\s*'
    m = re.match(regex, line)
    if not m:
        print(line)
        exit(-1)
    return m.group('netid', 'url', 'circleurl')


def test_circleCI(url):
    r = requests.get(url)
    assert r.ok
    if 'PASSED' in r.text:
        print("CircleCI passed!")
        return 0
    else:
        print("CircleCI failed.")
        return -1


def get_github_student_url(netid):
    """
    Obtain the student list from the github page. 
    """
    url = 'https://raw.githubusercontent.com/CT-CS5356-Fall2017/cs5356/master/README.md'
    r = requests.get(url)
    assert r.ok
    text = r.text
    for l in text.split('\n'):
        if netid in l:
            return extract_netid_and_url(l)
    return None, None, None


if __name__ == "__main__":
    USAGE = """
    $ python {0} -github <netid>    # To test the final submission
    or 
    $ python {0} <url>   # For just testing the url you created is working or not.
    """.format(sys.argv[0])
    netid=None
    r  = 0
    if len(sys.argv)<2:
        print(USAGE)
        exit(-1)
    if len(sys.argv)>2 and sys.argv[1] == '-github':
        netid, URL, circleurl = get_github_student_url(sys.argv[2])
        if not circleurl:
            print("Could not find circleurl={!r}".format(circleurl))
        else:
            r += test_circleCI(circleurl)
    else:
        URL = sys.argv[1]
    URL = URL.rstrip('/')
    print("The url found: {}".format(URL))
    if not URL.startswith('http'):
        print("The url does not look like one (should start with http..).\n"
              "May be you meant 'python {} -github {}".format(*sys.argv))
        exit(-1)
    r += test_netid(netid)
    if r==0:
        r = test_tag_association()
    if r==0:
        print("\nGreat everything worked!")
    else:
        print("Something is not right. See above")
