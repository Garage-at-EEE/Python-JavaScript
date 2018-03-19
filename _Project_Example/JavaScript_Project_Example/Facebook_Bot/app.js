'use strict';
const   bodyParser = require('body-parser'),
        config = require('config'),
        crypto = require('crypto'),
        express = require('express'),
        https = require('https'),
        request = require('request'),
        fs = require('fs'),
        app = express();

// const https = require('https');
// const options = {
//     key: fs.readFileSync("../cert/zaynjarvis.com.key"),
//     cert: fs.readFileSync("../cert/zaynjarvis_com.crt"),
//     ca: fs.readFileSync("../cert/zaynjarvis_com.ca-bundle")
// };
// https.createServer(options, app).listen(443)
const   Employees = require('./classes/employees'),
        Volunteers = require('./classes/volunteers'),
        Immigrants = require('./classes/immigrant'),
        Users = require("./classes/users"),
        { sendTextMessage, callSendAPI, sendTypingOn, sendTypingOff } = require('./tools');


let allUsers = {};

const association = {
    "employee": Employees,
    "volunteer": Volunteers,
    "immigrant": Immigrants
}

const APP_SECRET = (process.env.MESSENGER_APP_SECRET) ?
    process.env.MESSENGER_APP_SECRET :
    config.get('appSecret');
const VALIDATION_TOKEN = (process.env.MESSENGER_VALIDATION_TOKEN) ?
    (process.env.MESSENGER_VALIDATION_TOKEN) :
    config.get('validationToken');
const PAGE_ACCESS_TOKEN = (process.env.MESSENGER_PAGE_ACCESS_TOKEN) ?
    (process.env.MESSENGER_PAGE_ACCESS_TOKEN) :
    config.get('pageAccessToken');
const SERVER_URL = (process.env.SERVER_URL) ?
    (process.env.SERVER_URL) :
    config.get('serverURL');
// can delete upon deployment.
if (!(APP_SECRET && VALIDATION_TOKEN && PAGE_ACCESS_TOKEN && SERVER_URL)) {
    console.error("Missing config values");
    process.exit(1);
}
app.set('port', process.env.PORT || 8000);
app.set('view engine', 'ejs');
app.use(bodyParser.json({ verify: verifyRequestSignature }));
app.use(express.static('public'));

// app.get('/', function (request, response) {
//     response.sendFile('./index.html')
// })

app.listen(app.get('port'), function () {
    console.log('Node app is running on port', app.get('port'));
});

app.get('/webhook', function (req, res) {
    if (req.query['hub.mode'] === 'subscribe' &&
        req.query['hub.verify_token'] === VALIDATION_TOKEN) {
        console.log("Validating webhook");
        res.status(200).send(req.query['hub.challenge']);
    } else {
        console.error("Failed validation. Make sure the validation tokens match.");
        res.sendStatus(403);
    }
});

//-------------------------------------------------------------------------------------
//-------------------------------------------------------------------------------------
//-------------------------------------------------------------------------------------

app.post('/webhook', function (req, res) {
    let data = req.body;
    console.log(data);
    // Make sure this is a page subscription
    if (data.object == 'page') {
        data.entry.forEach(function (pageEntry) {
            let pageID = pageEntry.id;
            let timeOfEvent = pageEntry.time;
            let messagingEvent = pageEntry.messaging[0];
            let senderId = messagingEvent.sender.id;
            console.log('-----------------------------------------'+senderId);
            allUsers[senderId] = allUsers[senderId] ? allUsers[senderId] : new Users(senderId);
            if (messagingEvent.message) {
                allUsers[senderId].handleMessage(messagingEvent);
            }else if (messagingEvent.postback) {
                allUsers[senderId].receivedPostback(messagingEvent);
                if (allUsers[senderId].newStatus){
                    console.log(messagingEvent.postback.payload);
                    allUsers[senderId] = new association[messagingEvent.postback.payload](senderId);
                    console.log(allUsers[senderId].newStatus);
                    allUsers[senderId].welcome();
                }
                console.log(allUsers[senderId]);              
            }        
        });
        res.sendStatus(200);
    }
});
function verifyRequestSignature(req, res, buf) {
    var signature = req.headers["x-hub-signature"];

    if (!signature) {
        // For testing, let's log an error. In production, you should throw an 
        // error.
        console.error("Couldn't validate the signature.");
    } else {
        var elements = signature.split('=');
        var method = elements[0];
        var signatureHash = elements[1];

        var expectedHash = crypto.createHmac('sha1', APP_SECRET)
            .update(buf)
            .digest('hex');

        if (signatureHash != expectedHash) {
            throw new Error("Couldn't validate the request signature.");
        }
    }
}
module.exports = app;