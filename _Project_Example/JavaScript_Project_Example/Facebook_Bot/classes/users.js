const { sendTextMessage, callSendAPI, sendTypingOn, sendTypingOff, SERVER_URL } = require('../tools');
class Users{
    constructor(id){
        this.id = id;
        this.name = '';
        this.newWork = '';
        this.newStatus = false;
    } 
    
    handleMessage() {
        this.welcome();
    }
    receivedPostback(event) {
        let text;
        // var recipientID = event.recipient.id;
        // var timeOfPostback = event.timestamp;// can import time to db if have one.
        var payload = event.postback.payload;
        if (payload === 'immigrant' || payload === 'volunteer' || payload === 'employee')
            {
                this.newStatus = true;
                this.newWork = payload;// CHANGE TO PROMISE!
                console.log('match------------------------------'+this.newWork);
                text = "Now, you are our "+payload;
            };
        sendTextMessage(this.id, text);
    }

    welcome() {
        var messageData = {
            recipient: {
                id: this.id
            },
            message: {
                attachment: {
                    type: "template",
                    payload: {
                        template_type: "button",
                        text: "Hi! Can I help you?",
                        buttons: [
                        {
                            type: "postback",
                            title: "I am an immigrant.",
                            payload: "immigrant"
                        }, {
                            type: "postback",
                            title: "I am a volunteer.",
                            payload: "volunteer"
                        }, {
                            type: "postback",
                            title: "I am an employee.",
                            payload: "employee"
                        }]
                    }
                }
            }
        };
        callSendAPI(messageData);
    }
    contact() {
        var messageData = {
            recipient: {
                id: recipientId
            },
            message: {
                attachment: {
                    type: "template",
                    payload: {
                        template_type: "button",
                        text: "Contact Us!",
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
module.exports = Users;