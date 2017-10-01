'use strict';

const puppeteer = require('puppeteer');

// const url = "http://ec2-13-59-91-251.us-east-2.compute.amazonaws.com:8080/";
// const url = "http://ec2-13-59-20-128.us-east-2.compute.amazonaws.com:8080/";
const video_url = [
    './receipt_vid.y4m',
    './cappones.y4m'
];
const receipt_texts = [
    {"merchant":"Main Street Restaurant", "amount": "29.01", "tags": []},
    {"merchant":"Cappones", "amount": "28.86", "tags": []}
]
const video_idx = 0 // Math.floor(Math.random() * 2); // cappones does not work

function rand_string(n) {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for (var i = 0; i < n; i++)
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    return text;
}

async function add_receipt(page) {
    var rcpt = {
        merchant: 'M_' + rand_string(4),
        amount: (Math.floor(Math.random() * 10000)/100.0).toString(),
        tags: []
    }
    await page.click('#add-receipt');
    // Enter merchant
    await page.click('#merchant');
    await page.type(rcpt.merchant);

    // Enter amount
    await page.click('#amount');
    await page.type(rcpt.amount);

    await page.click('#save-receipt');
    return rcpt;
}

function add_tag(i, tag) {
    var sel = '#receiptList .receipt';
    var rcpt_elem = $(sel)[i];
    // alert(rcpt_elem + ' --> ' + sel + ' --> ' + i);
    var e_up = jQuery.Event("keyup", {which: 13, keyCode: 13});
    var e_press = jQuery.Event("keypress", {which: 13, keyCode: 13});
    $('.add-tag', rcpt_elem).click();
    $('.tag_input', rcpt_elem).val(tag).trigger(e_up).trigger(e_press);
    console.log($('.tagValue', rcpt_elem).text());
}

function del_tag(i) {
    const sel = '#receiptList .receipt';
    const rcpt_elem = $(sel)[i];
    // alert(rcpt_elem + ' --> ' + sel + ' --> ' + i);
    const e_up = jQuery.Event("keyup", {which: 13, keyCode: 13});
    const e_press = jQuery.Event("keypress", {which: 13, keyCode: 13});
    const tags = $('.tagValue', rcpt_elem);
    const j = Math.floor(Math.random() * tags.length);
    const tag_val = $(tags[j]).text();
    $(tags[j]).click();
    return tag_val;
}



function test_addition(oldl, newl, addition, thing='', ret_log={}) {
    /* Tests if the additional element is in the newl */
    let failed = 0;
    if (newl.length != oldl.length + 1) {
        ret_log['msg'] += "Number of added " + thing + " did not match. ";
        console.log(JSON.stringify(oldl));
        console.log(JSON.stringify(newl));
        failed = 1;
        ret_log['failed'] = failed;
        return ret_log;
    }
    let found = 0;
    let i;
    for(i=0; failed == 0 && i<newl.length; i++) {
        if (JSON.stringify(newl[i]) == JSON.stringify(addition)) {
            found = 1; break;
        } else {
            console.log([newl[i], addition].map(JSON.stringify))
        }
    }
    if (found == 0) {
        failed = 1;
        ret_log['msg'] += "Could not find the " + thing + " just added."
        console.dir(newl);
    } else {
        ret_log['msg'] = "Test passed!!"
    }
    ret_log['failed'] = failed;
    return ret_log;
}
    
async function test_add_receipt(page) {
    const curr_rcpts = await page.evaluate(get_receipts);
    const added_rcpt = await add_receipt(page);
    const new_rcpts = await page.evaluate(get_receipts);
    var ret_log = {
        test : "<--- Running add_receipt test --->",
        msg : '',
        action: {
            'added_receipt': added_rcpt
        }
    }
    ret_log = test_addition(curr_rcpts, new_rcpts, added_rcpt, 'receipt', ret_log);
    return ret_log;
}

function get_tags(i) {
    const rcpt_elem = document.querySelectorAll('#receiptList .receipt')[i];
    const anchors = Array.from(rcpt_elem.querySelectorAll('.tags .tagValue'));
    return anchors.map(anchor => anchor.textContent);
}

async function test_del_tag(page) {
    var rcpts = await page.$$('.receipt');
    var i = Math.floor(Math.random() * rcpts.length);
    var new_tags = await page.evaluate(get_tags, i);
    while (new_tags.length == 0) {
        await page.evaluate(add_tag, i, 't_' + rand_string(4));
        new_tags = await page.evaluate(get_tags, i);
	console.log("Tags before deletion:", new_tags);
    }
    // Delete tag experiment
    var deleted_tag = await page.evaluate(del_tag, i);
    var tags_after_deletion = await page.evaluate(get_tags, i);
    var ret_log = {
        test : "<--- Running del_tag test --->",
        msg : '',
        action: {
            'deleted_tag': deleted_tag
        }
    }

    ret_log = test_addition(
        tags_after_deletion, new_tags, deleted_tag, 
        'tag', ret_log
    )
    return ret_log;
}

async function test_add_tag(page) {
    var tag = {tag: 't_' + rand_string(4)};
    // Sample a random receipt
    var rcpts = await page.$$('.receipt');
    var i = Math.floor(Math.random() * rcpts.length);

    var ret_log = {
        test : "<--- Running add_tag test --->",
        msg : '',
        action: {
            'add_tag_at_receipt': [tag.tag, i]
        }
    }
    // Add tag experiment
    console.log("Adding tag", i)
    const old_tags = await page.evaluate(get_tags, i);
    await page.evaluate(add_tag, i, tag.tag);
    const new_tags = await page.evaluate(get_tags, i);
    var x_mark = ' x';
    if (!new_tags[0].endsWith(' x'))
        x_mark = '';
    ret_log = test_addition(
        old_tags, new_tags, tag.tag + x_mark, 
        'tag', ret_log
    ) 
    
    return ret_log;
}


function take_snap() {
    $('#start-camera').click(() => {
        console.log("clicked...start camera...");
        setTimeout(() => {
            $('#take-pic').click(() => {
                setTimeout(() => {
                    $('#save-receipt').click();
                }, 2);
            }, 1);
        });
    });
}

async function test_snap(page) { 
    const added_rcpt = receipt_texts[video_idx];
    var ret_log = {
        test : "<--- Running snap_receipt test --->",
        msg : '',
        action: {
            'snap_receipt_from_video': video_url[video_idx],
            'expected_receipt': added_rcpt
        }
    }
    const curr_rcpts = await page.evaluate(get_receipts);
    // await page.evaluate(take_snap);
    await page.click('#start-camera')
    console.log("Started the work...");
    await page.click('#take-pic');
    try {
        await page.waitForFunction('$("#merchant").val() != ""', 
                                   {timeout: 10000})
    } catch (e) {
        ret_log['msg'] = "I could not take a snap of the receipt. " + 
            "Common fix is to use `grabFrame` instead of `takePhoto`.";
        ret_log['failed'] = 1;
        return ret_log;
    }

    await page.waitForSelector('#save-receipt', {visible: true}).then(
        () => page.click('#save-receipt')
    );
    const new_rcpts = await page.evaluate(get_receipts);
    ret_log = test_addition(
        curr_rcpts, new_rcpts, added_rcpt,
        'receipt', ret_log
    );
    return ret_log;
}


function get_receipts() {
    function get_tags(rcpt_elem) {
        const anchors = Array.from(rcpt_elem.querySelectorAll('.tags .tagValue'));
        return anchors.map(anchor => anchor.textContent);
    }

    const anchors = Array.from(document.querySelectorAll('#receiptList .receipt'));
    return anchors.map(function(anchor) {
        return {
            merchant: anchor.querySelector('.merchant').textContent,
            amount: anchor.querySelector('.amount').textContent,
            tags: get_tags(anchor)
        }
    });
}

var test_func_list = {
    add_receipt: test_add_receipt,
    add_tag: test_add_tag,
    del_tag: test_del_tag,
    add_receipt_by_snap: test_snap
}
    
async function runTest(url, tests=[]) {
    const browser = await puppeteer.launch({
        headless: true, 
        slowMo: 100,
        userDataDir: '/tmp/test/',
        args: [
            '--unsafely-treat-insecure-origin-as-secure='+url,
            '--use-fake-device-for-media-stream',
            '--use-file-for-fake-video-capture=' + video_url[video_idx],
        ]        
    });
    try {
        browser.version().then(msg => console.log(msg));
        
        const page = await browser.newPage();
        await page.goto(url, {waitUntil: 'networkidle'});
        page.on('console', msg => console.log('PAGE LOG:', msg));

        await page.waitForSelector('.receipt');
        var ret_log = {};
        for(var i=0; i<tests.length; i++) {
            var k = tests[i];
            var f = test_func_list[k];
            if (!f) {
                return("Invalid test names: " + k);
            }
            ret_log[k] = await f(page);
        };
        console.log(ret_log);
        return ret_log;
    }
    catch (e) {
        console.dir(e);
        return("Something went wrong. Try refreshing the page");
    }
    finally {
        await browser.close();
    }
}
    


// Include it and extract some methods for convenience
const express = require('express');
const path    = require('path');
const morgan = require('morgan');
const fs = require('fs');

const app = express();

// For enabling logging
app.use(morgan('common', {
    stream: fs.createWriteStream('./access.log', {flags: 'a'})
}));
app.use(morgan('dev'));


// routes
app.get('/test', function (req, res) {
    console.log("Input:", req.query)
    var url = req.query.url;
    var tests = req.query.tests;
    if (typeof tests === 'string'){
        tests = [tests];
    }
    console.log("url:", url, '   tests:', tests);

    if (!url.startsWith('http')) {
        res.send("You url is malformed: " + url);
    } else {
        runTest(url, tests).then(ret => {
            var json_ret = JSON.stringify(ret, null, 4);
            res.send(req.query.url + '<br/><pre>' + json_ret + '</pre>')
        });
    }
})

app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
});

// Start the server
app.listen(8080, function () {
  console.log('Server listening on port 8080!')
});

