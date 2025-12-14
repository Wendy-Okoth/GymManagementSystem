const path = require('path');

module.exports = {
  entry: './assets/js/calendar.js',   // your custom JS entry
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'static/js'),
  },
  mode: 'development',
};
