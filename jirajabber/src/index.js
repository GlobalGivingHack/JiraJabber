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

  'UpdateStatus': function() {
    const slots = this.event.request.intent.slots;
    const ticketId = slots.TicketId.value;
    const status = slots.Status.value;

    updateStatus(ticketId, status, updateStatusCallback.bind(this));
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
  const story = {
    subject: summary,
    issuetype: jiraType
  };

  return callJiraLambda("create", story, callback);
}

function updateStatusCallback(ticket) {
  this.emit(':tell', "updated");
}
function updateStatus(ticketId, status, callback) {
  const story = {
    key: ticketId,
    status: status
  };

  return callJiraLambda("status_change", story, callback);
}

function callJiraLambda(action, story, callback) {
  var lambda = new aws.Lambda({
    region: 'us-west-2' //change to your region
  });

  const payload = {
    action: action,
    data: story
  };

  lambda.invoke({
    FunctionName: 'jiraIntegration',
    Payload: JSON.stringify(payload) // pass params
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