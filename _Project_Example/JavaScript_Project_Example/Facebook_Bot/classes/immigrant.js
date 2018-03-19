const Users = require('./users');
const { sendTextMessage, callSendAPI, sendTypingOn, sendTypingOff, SERVER_URL } = require('../tools');
class Immigrants extends Users {
    constructor(id) {
        super(id);
        this.newWork = '';
        this.newStatus = false;
        this.name = "immigrant";
        this.structure = {};
    }
    handleMessage() {

    }
    receivedPostback(event) {
        // The 'payload' param is a developer-defined field which is set in a postback 
        // button for Structured Messages. 
        var payload = event.postback.payload;
        this.structure[payload]();

        // When a postback is called, we'll send a message back to the sender to 
        // let them know it was successful
        sendTextMessage(this.id, "Postback called");
    }


}
module.exports = Immigrants;