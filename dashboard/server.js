const db = require("./db-connection.js");
const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const infoCtrl = require("./controllers/info");

app.set('view engine','ejs');
app.use('/public', express.static(__dirname + '/public'));

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));

app.get('/dashboard', function(req,res){
  infoCtrl.all_tweets()
  .then((tweets) => {
    infoCtrl.all_words()
    .then((words) => {
      let sentiments = tweets.map(x => x.sentiment);
      let results = sentiments.reduce((a, c) => (a[c] = (a[c] || 0) + 1, a), Object.create(null));
      res.render('dash',{tweets: tweets, words: words, sentiments: results});
    })
    .catch((err) =>{
      console.log(err)
      res.send("Banco de dados deu problema");
    });
  })
  .catch((err) =>{
    res.send("Banco de dados deu problema");
  });
})

app.listen(3097,function(){
  console.log("Ouvindo a porta 3097!");
})
