const Users = require('./users');
const { sendTextMessage, callSendAPI, sendTypingOn, sendTypingOff, SERVER_URL } = require('../tools');
class Volunteers extends Users {
    constructor(id) {
        super(id);
        this.newWork = '';
        this.newStatus = false;
        this.name = "volunteer";
        this.structure = {
            "Join The Recent Event": this.recentEvent,
            "Join The SDI Volunteer Society": this.joinSociety,
            "volunteer": this.welcome
        };
    }
    handleMessage() {
        this.welcome();
    }
    receivedPostback(event) {
        // var timeOfPostback = event.timestamp;
        // The 'payload' param is a developer-defined field which is set in a postback 
        // button for Structured Messages. 
        var payload = event.postback.payload;
        this.structure[payload]();

        // When a postback is called, we'll send a message back to the sender to 
        // let them know it was successful
        sendTextMessage(this.id, "Postback called");
    }
    welcome(){
        var messageData = {
            recipient: {
                id: this.id
            },
            message: {
                attachment: {
                    type: "template",
                    payload: {
                        template_type: "generic",
                        elements: [{
                            title: "Thank you for being a volunteer",
                            subtitle: "We assure you a great volunteer experience",
                            image_url: "http://kids.mbcgateway.ca/wp-content/uploads/2014/07/volunteer-icon.jpg",
                            buttons: [{
                                type: "web_url",
                                url: "https://www.sdi-academy.org/",
                                title: "Open Our Website"
                            }, {
                                type: "postback",
                                title: "Join The Recent Event",
                                payload: "Join The Recent Event"
                            }, {
                                type: "postback",
                                title: "Join The SDI Volunteer Society",
                                payload: "Join The SDI Volunteer Society"
                            }],
                        }]
                    }
                }
            }
        };
        callSendAPI(messageData);
    }
    recentEvent() {

    }
    joinSociety() {

    }
}
module.exports = Volunteers;