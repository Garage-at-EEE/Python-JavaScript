const Users = require('./users');
const { sendTextMessage, callSendAPI, sendTypingOn, sendTypingOff, SERVER_URL } = require('../tools');
class Employees extends Users {
    constructor(id){
        super(id);
        this.newWork = '';
        this.newStatus = false;
        this.name = "employee";
        this.structure = {
            "employee": this.welcome,
            //other key and function pairs
        };
    }
    handleMessage(){
        this.welcome();
    }
    receivedPostback(event) {
    var timeOfPostback = event.timestamp;// can import time to db if have one.
    var payload = event.postback.payload;
    this.structure[payload]();
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
                        template_type: "button",
                        text: "Contact the boss",
                        buttons: [
                            {
                                type: "web_url",
                                url: "https://www.sdi-academy.org/",
                                title: "Open Web URL"
                            }, {
                                type: "phone_number",
                                title: "Call Phone Number",
                                payload: "+65xxxxxxxx"
                            }
                        ]
                    }
                }
            }
        };
        callSendAPI(messageData);
    }
}
module.exports = Employees;