const bst = require('bespoken-tools');
const chai = require('chai');
const test = require('./initTests.js');

const expect = chai.expect;


describe('Alexa Jira Jabber', function() {
  it('launches and starts', function(done) {
    launchSkill()
      .then((payload) => done())
      .catch((e) => {
        console.error(e);
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