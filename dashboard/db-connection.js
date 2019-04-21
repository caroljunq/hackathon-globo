const mongoose = require("mongoose");

mongoose.Promise = global.Promise;

mongoose.connect("mongodb://hack:hack123@ds057944.mlab.com:57944/hack_globo", { useNewUrlParser: true },function(err){
  if(err){
    console.log(err);
  }
});
