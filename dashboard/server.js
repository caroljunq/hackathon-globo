const db = require("./db-connection.js");
const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const infoCtrl = require("./controllers/info");

app.use('/public', express.static(__dirname + '/public'));

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));

app.get('/tweets', function(req,res){
  infoCtrl.all_tweets()
  .then((tweets) => {
    res.send(tweets);
  })
  .catch((err) =>{
    res.send("Banco de dados deu problema");
  });
})

app.get('/words', function(req,res){
  infoCtrl.all_words()
  .then((words) => {
    res.send(words);
  })
  .catch((err) =>{
    console.log(err)
    res.send("Banco de dados deu problema");
  });
})

app.listen(3097,function(){
  console.log("Ouvindo a porta 3097!");
})
