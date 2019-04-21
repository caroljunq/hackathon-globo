const mongoose = require("mongoose");

let tweetSchema = new mongoose.Schema({
  text: {
    type: String,
    required: true
  },
  sentiment: {
    type: String,
    required: true
  },
  user: {
    type: String,
    required: true
  },
}, { collection: 'tweets' });

module.exports = mongoose.model('TweetSchema', tweetSchema);
