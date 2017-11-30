const bst = require('bespoken-tools');
const chai = require('chai');
const test = require('./initTests.js');

const expect = chai.expect;


describe('Alexa Jira Jabber', function() {
  // it('launches and starts', function(done) {
  //   launchSkill()
  //     .then((payload) => done())
  //     .catch((e) => {
  //       console.error(e);
  //     });
  // });

  it('should update status', function(done) {
    test.alexa.intended('UpdateStatus', { "TicketId": "JJ-11", "Status": "Todo" }, function(error, payload) {
      console.log(payload);
      // expect(payload.response.outputSpeech.ssml)
      //   .to.contain("Player 3, its your move");

      done();
    });    
  });
});

function launchSkill() {
  return new Promise((resolve, reject) => {
    test.alexa.launched(function(error, payload) {
      console.log(payload.response);
      expect(payload.response.outputSpeech.ssml)
        .to.contain('Welcome to Jira');

      resolve(payload);
    });
  });
}