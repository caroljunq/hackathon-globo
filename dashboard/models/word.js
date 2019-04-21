const mongoose = require("mongoose");

let wordSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true
  },
  value: {
    type: String,
    required: true
  },
}, { collection: 'words' });

module.exports = mongoose.model('WordSchema', wordSchema);
