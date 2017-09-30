const rp = require('request-promise');
const fs  = require("fs");
const cheerio = require('cheerio');

var lines = fs.readFileSync('../README.md').toString().split('\n');
var re = /([a-z]{2,3}[0-9]{2,4}) ?- ?\[(htt[^\]]*)\]/;


var x = 0;
lines.forEach(line => {
  //if(x == 10)
   // return;

  //console.log(lines[i]);
  var matches = re.exec(line);
  if(matches && !matches[2].endsWith('grading.html')) {
    console.log(`${matches[1]} \t ${matches[2]}`);
    var netid = matches[1];
    var url = matches[2];

    //if(netid != 'rs2468')
     // return;

    var options = {
      uri: url,
      headers: {
        'Accept': 'text/html'
      },
      transform: function (body) {
        return cheerio.load(body);
      }
    };

    rp(options).then($ => {
      //console.log($.html());
      //console.log(`---------- ${netid} -----------`);
      // check out the script tags
      var rv = '';
      $('script').each((i, script) => {
         var src = $(script).attr('src');
         var contents = $(script).contents() ? $(script).contents().text() : '';

         //console.log(script);

	 if(!src) {
           if(script.type !== 'script' || contents.trim()[0] === '<')
             return true;

	   rv += '\n' + $(script).contents().text();
           return true;
         } else if(!/react|min\.js|notify|jquery/.test(src)) {
	   console.log('DOWNLOADING: '+ url+'/'+src);
           rv = rp(url+'/'+src);
           return false;
	 }
      });

      return rv;
    })
    .then(script => {
      if(script === '')
        console.log(`${netid} got nothing`);
      else {
        console.log(`${netid} Got a script`);
        fs.writeFile(`./output/${netid}.js`, script);
      }
    })
    .catch(function(xhr){
      if(xhr.statusCode)
        console.log(`${netid} failed with ${xhr.statusCode}`);
      else if(xhr.name === 'RequestError') {
        console.log(`${netid} got ${xhr.name}`);
      } else {
	console.log(`${netid} failed `);
        console.log(xhr);
      };
    });

    x++;
  }

});
