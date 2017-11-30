'use strict';

const Alexa = require('alexa-sdk');
const Speech = require('ssml-builder');

exports.handler = function(event, context, callback) {
  const alexa = Alexa.handler(event, context);
  alexa.registerHandlers(handlers);
  alexa.execute();
};

const handlers = {
  'LaunchRequest': function () {
    this.emit(':tell', 'Welcome to Jira Jabber');
  },

  'AMAZON.CancelIntent': function () {
      this.response.speak('Goodbye!');
      this.emit(':responseReady');
  },
  'AMAZON.StopIntent': function () {
      this.response.speak('See you later!');
      this.emit(':responseReady');
  }
};