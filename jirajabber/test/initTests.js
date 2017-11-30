const chai = require('chai');
const bst = require('bespoken-tools');

const test = {
  server: null,
  alexa: null
};

beforeEach(function(done) {
  test.server = new bst.LambdaServer('../src/index.js', 10000, true);
  test.alexa = new bst.BSTAlexa('http://localhost:10000',
                            '../../alexa/intents.json',
                            '../../alexa/utterances.txt');

  test.server.start(function() {
    test.alexa.start(function(error) {
      if (error !== undefined) {
        console.error('Error: ' + error);
      }
      else {
        done();
      }
    });
  });
});

afterEach(function(done) {
  test.alexa.stop(function() {
    test.server.stop(function() {
      done();
    });
  });
});

module.exports = test;