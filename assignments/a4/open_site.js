#!/usr/local/bin/node

const rp = require('request-promise');
const _ = require('lodash');

function die(msg) {
  console.log(msg);
  process.exit(1);
}

if(process.argv.length !== 3)
  die('wrong args');

let netid = process.argv[2];
if(!/[a-z]+[0-9]+/.test(netid))
  die(`"${netid}" not a netid`);

rp.get('https://raw.githubusercontent.com/CT-CS5356-Fall2017/cs5356/master/README.md')
.then(html => {
  console.log(`searching site for ${netid}`);
  let re = new RegExp(`^.+${netid}.+$`);
  let matches = _.filter(html.split('\n'), line => line.match(re));

  if(matches.length === 0)
    die('no results found');

  if(matches.length > 1)
    die('too many results found');

  let line = matches[0];
  matches = line.match(/http[^\]]+/);
  if(matches.length !== 1)
    die('could not extract url');

  var url = matches[0];
  console.log(`spawning chromium with ${url}`);
  let cp = require('child_process').spawn(
    './node_modules/puppeteer/.local-chromium/mac-499413/chrome-mac/Chromium.app/Contents/MacOS/Chromium',
    [
      `--unsafely-treat-insecure-origin-as-secure=${url}`,
      `--use-file-for-fake-video-capture=cappones.y4m`,
      `--use-fake-ui-for-media-stream`,
      `--use-fake-device-for-media-stream`,
      `--user-data-dir=/tmp/bzz`,
      `${url}`
    ],
    {
      detach: true,
      stdio: 'ignore'
    }
  );
  cp.unref();
});
