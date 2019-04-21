const Tweet = require('../models/tweet');
const Word = require('../models/word');

function all_tweets(){
  return Tweet.find();
}

function all_words(){
  return Word.find();
}


module.exports.all_tweets = all_tweets;
module.exports.all_words = all_words;
