const https = require('https')
const { stringReplace } = require('string-replace-middleware')
var express = require('express');

const ip_listen = process.argv[2] ?? "127.0.0.1"; 
const port_listen = process.argv[3] ?? 8080; 
const ip_api = process.argv[4] ?? "127.0.0.1"; 
const port_api = process.argv[5] ?? 3001; 

process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";
var app = express()

app.use(stringReplace({
	'%%IP%%' : ip_listen,
	'%%PORT%%' : port_listen
}));

app.get('/', function (req, res) {
    try {
        res.sendFile('public/index.html', { root: __dirname });
    } catch (error) {
        console.log(error);   
    }
});

app.get('/map', async function(req, res) {
    try {
        var request = https.request({ 
            host: ip_api, 
            port: port_api,
            path: '/fwq/map',
            method: 'GET',
            rejectUnauthorized: false,
            requestCert: true,
            agent: false
          }, (response) => {
            console.log('statusCode:', response.statusCode);
            console.log('headers:', response.headers);
          
            response.on('data', (d) => {
                process.stdout.write(d);
                res.status(200).header({"content-type" : "application/json"}).send(d);
            });

            response.on('error', function(error) {
                res.status(500).send(error);
            });
          }
        ).on('error', (error) => { 
            res.status(500).send(error); 
        });
        request.end();
    } catch (error) {
        res.status(500).send(error);
    }
})

const fs = require('fs');
const httpsOptions = {
    key: fs.readFileSync('./key.pem'),
    cert: fs.readFileSync('./cert.pem')
}

const server = https.createServer(httpsOptions, app).listen(port_listen, ip_listen, () => {
    console.log('Server listening in ' + ip_listen + ":" + port_listen);
});
