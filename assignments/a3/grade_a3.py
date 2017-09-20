import sys
import requests
import random
import string
import re
import time

try:
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
except ImportError:
    print("""
Install selenium for python. `pip install -U selenium`. You also have to download 
Selenium Gecko Webdirver binary from https://github.com/mozilla/geckodriver/releases.
 
How to install this driver can be found https://selenium-python.readthedocs.io/installation.html#drivers.\n
For Linux and Mac, you can just unzip and copy the driver into /usr/local/bin/. 
For Windows, you can follow the instructions in the page.
""")
    exit(-1)

DEBUG = 1
def random_tag(n=4):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) 
                   for _ in range(n))


def get_tags(receipt_e):
    return [
        t.text
        for t in receipt_e.find_elements_by_class_name('tagValue')
    ]


def get_all_receipts(driver):
    """
    Parse all the receipts in a page
    $($('#receiptList')[0], '.receipt')
    """
    for rs in driver.find_elements_by_css_selector('#receiptList > .receipt'):
        m = rs.find_element_by_class_name('merchant').text
        a = rs.find_element_by_class_name('amount').text
        tags = get_tags(rs)
        # created = rs.find_element_by_class_name('created').text
        yield {
            'merchant': m,
            'amount': a,
            'tags': tags,
            # 'created': created
        }
    

def add_receipts(driver):
    e = driver.find_element_by_id('add-receipt')
    e.click()
    m = 'M__' + random_tag(3)
    a = int(random.random() * 10000)/100
    driver.find_element_by_id('merchant').send_keys(str(m))
    driver.find_element_by_id('amount').send_keys(str(a))
    driver.find_element_by_id('save-receipt').click()
    return m, a


def add_tag(e):
    """ Adds a random tag to te element e """
    tag = random_tag(8)
    e.find_element_by_class_name('add-tag').click()
    
    e.find_element_by_class_name('tag_input')\
          .send_keys(tag)
    e.find_element_by_class_name('tag_input')\
          .send_keys(Keys.ENTER)
    # driver.find_elements_by_class_name('save-tag').click()
    return tag

def set_up(url):
    driver = webdriver.Firefox()
    driver.implicitly_wait(1)
    driver.get(url)
    return driver

def test_add_receipts(driver):
    """
    Adds a receipt and checks if the receipt is available in the page 
    or not.
    """
    print("-"*80)
    print("Test: Adding a receipt")
    print("-"*80)

    driver = driver
    time.sleep(1)
    old_receipts = list(get_all_receipts(driver))
    m, a = add_receipts(driver)

    if DEBUG>=2:
        driver.refresh()
    time.sleep(1)
    new_receipts = list(get_all_receipts(driver))
    if len(old_receipts) + 1 != len(new_receipts):
        print("old_receipts={}\n>> new_receipts={}"
              .format(old_receipts, new_receipts))
        return -1
    found = False
    if DEBUG:
        print("#receipts-old: {}, #receipts-new: {}"
              .format(len(old_receipts), len(new_receipts)))
    for i, rs in enumerate(new_receipts):
        if str(rs['merchant']) == str(m) and str(rs['amount']) == str(a):
            found = True
            break
        elif DEBUG:
            print("{}. Found (but not testing): {}".format(i, rs))

    if not found:
        print(
            "ERROR: I don't see the receipt I just inserted with \n"
            "merchant={!r} and amount={!r}".format(m, a)
        )
        return -1
    print("Success!!!")
    print('<>'*40 + '\n')
    return 0

def test_add_tag(driver):
    """
    Adds tag to a randomly chosen receipts, and test if the tag appears in
    the page.
    """
    print("-"*80)
    print("Test: Adding a tag")
    print("-"*80)

    time.sleep(1)
    # Get all receipts
    receipts = driver.find_elements_by_class_name('receipt')

    # Choose a receipt randomly to add tag 
    i = random.randint(0, len(receipts)-1)
    e = receipts[i]

    # Click on the add-tag element
    old_tags = get_tags(e)
    tag = add_tag(e)
    if DEBUG>=2:
        driver.refresh()   # Probably don't require

    time.sleep(4)
    # Fetch the new receipts again
    receipts = driver.find_elements_by_class_name('receipt')
    e = receipts[i]

    new_tags = get_tags(e)
    added_tags_ = list(set(new_tags) - set(old_tags))
    if len(added_tags_) != 1 or tag not in added_tags_[0]:
        print("""
ERROR: The number of newly added tags did not match.
Expected: {!r},           Found: {!r}""".format([tag], added_tags_))
        return -1
    print("Success!!!")
    print('<>'*40 + '\n')
    return 0


def test_del_tag(driver):
    """
    Selects a random receipt and delets its one of the tag.
    """
    print("-"*80)
    print("Test: Deleting a tag")
    print("-"*80)
    # Select a random receipt
    receipts = driver.find_elements_by_class_name('receipt')
    index_of_random_receipt = random.randint(0, len(receipts)-1)
    e = receipts[index_of_random_receipt]

    # Click on the add-tag element
    tags = get_tags(e)
    if not tags:
        add_tag(e)
        receipts = driver.find_elements_by_class_name('receipt')
        e = receipts[index_of_random_receipt]
        tags = get_tags(e)

    time.sleep(1)
    e_tag = random.choice(e.find_elements_by_class_name('tagValue'))
    tag = e_tag.text
    e_tag.click(); time.sleep(1)

    # Receipts DOM might have been deleted or re-drawn, pull it again
    receipts = driver.find_elements_by_class_name('receipt')
    e = receipts[index_of_random_receipt]
    new_tags = get_tags(e)
    removed_tag_ = list(set(tags) - set(new_tags))
    if len(removed_tag_) != 1 or removed_tag_[0] != tag:
        print(""" Removed tags: {} (Should be only [{}])"
        """.format(removed_tag_, tag))
        print("""This error might not be your fault. Either my code or the Selenium driver is
buggy.  Report this problem to us. We will fix it, but in the mean time make
sure the deletion works on UI, and no more errors are reported before this line.
        """)
        return -1
    else:
        print("Success!!!")
        print('<>'*40 + '\n')
        return 0

def test_no_duplicate_tag(driver):
    """
    Tests that no duplicate tags are present in any of the receipt rows.
    """
    print("-"*80)
    print("Test: Duplicate tag in any receipt")
    print("-"*80)
    
    for i,rs in enumerate(driver.find_elements_by_class_name('receipt')):
        l = list(get_tags(rs))
        if len(l) != len(set(l)):
            print("There are duplicate tags in the {}-th receipt line"\
                  .format(i))
            print("Found tag: {!r}".format(l))
            return -1
    print("Success!!!")
    print('<>'*40 + '\n')
    return 0

def tearDown(driver):
    driver.quit()

def extract_netid_and_url(line):
    regex = r'\* \[.*\]\(.*\) - (?P<netid>\w+) \- \[.+\]\((?P<url>http.+)\)\s*\[\!\[CircleCI\]\((?P<circleurl>.*)\)\]\(.*\)\s*'
    m = re.match(regex, line)
    if not m:
        print(line)
        exit(-1)
    return m.group('netid', 'url', 'circleurl')

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
    # Parse commandline
    USAGE = """
    $ python {0} -github <netid>    # To test the final submission
    or 
    $ python {0} <url>   # For just testing the url you created is working or not.
    """.format(sys.argv[0])
    url = None
    netid=None
    r  = 0
    if len(sys.argv)<2:
        print(USAGE)
        exit(-1)
    if len(sys.argv)>2 and sys.argv[1] == '-github':
        netid, url, circleurl = get_github_student_url(sys.argv[2])
    else:
        url = sys.argv[1]
    driver = set_up(url)
    r = 0
    try:
        r += 1 + test_add_receipts(driver)
        if (r>=0):
            r += 1 + test_add_tag(driver)
        if (r>0):
            r += 1 + test_del_tag(driver)
        if (r>0):
            r += 1 + test_no_duplicate_tag(driver)
    except (AssertionError, ImportError) as e:
        print("=======")
        print("Error:", e)
        print("=======\n")
        print("Something went wrong. Test the each of the tests manually and make sure it\n"
              "is working. If yes, check the IDs and class names in your html\n"
              "file matches what is dictated in the README file.\n\n"
              "Meaning of some of the common errors. \n")
        print("\"Element not visible\": Your server might be too slow. Find the line\n"
              "'implicitly_wait' in the auto-grader and change the wait time from\n"
              " 5 sec to something more like 15 or 20.")

    finally:
        tearDown(driver)
