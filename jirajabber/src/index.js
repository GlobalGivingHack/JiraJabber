'use strict';

const Alexa = require('alexa-sdk');
const Speech = require('ssml-builder');
const aws = require('aws-sdk');

exports.handler = function (event, context, callback) {
  const alexa = Alexa.handler(event, context);
  alexa.registerHandlers(handlers);
  alexa.execute();
};

const handlers = {
  'LaunchRequest': function () {
    this.emit(':tell', 'Welcome to Jira Jabber');
  },
  'CreateStory': function () {
    const storySummary = this.event.request.intent.slots.StorySummary.value;
    let handler = this;
    createStory(storySummary, emitCallback.bind(this));
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

function emitCallback() {
  this.emit(':tell', "I just created a new story with ticket number 123");
}

function createStory(storySummary, callback) {
  var lambda = new aws.Lambda({
    region: 'us-west-2' //change to your region
  });

  let story = {
    "subject": storySummary
  }

  lambda.invoke({
    FunctionName: 'jiraIntegration',
    Payload: JSON.stringify(story) // pass params
  }, function (error, data) {
    if (error) {
      console.log('error', error);
    }
    if (data.Payload) {
      console.log(data.Payload);
      callback(data.Payload);

    }
  });

}

