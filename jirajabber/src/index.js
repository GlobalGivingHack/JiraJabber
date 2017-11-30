'use strict';

const Alexa = require('alexa-sdk');
const Speech = require('ssml-builder');
const aws = require('aws-sdk');

var summary;
var jiraType;

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
    summary = this.event.request.intent.slots.Summary.value;
    jiraType = this.event.request.intent.slots.JiraType.value;
    let handler = this;
    createStory(emitCallback.bind(this));
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

function emitCallback(ticket) {
  console.log("ticket: " + ticket);
  this.emit(':tell', "I just created a new " + jiraType + " with id " + ticket.key);
}

function createStory(callback) {
  var lambda = new aws.Lambda({
    region: 'us-west-2' //change to your region
  });

  let story = {
    'action': 'create',
    'data': {
      "subject": summary,
      "issuetype": jiraType
    }
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
      callback(JSON.parse(data.Payload));

    }
  });

}

