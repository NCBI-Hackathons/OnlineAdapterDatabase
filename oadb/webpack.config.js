var path = require("path");
var BundleTracker = require('webpack-bundle-tracker');
var WebpackCleanup = require('webpack-cleanup-plugin');

module.exports = {
    context: __dirname,

    entry: './app/js/index',

    output: {
        path: path.resolve('./app/bundles'),
        filename: "[name]-[hash].js"
    },

    plugins: [
        new BundleTracker({filename: './webpack-stats.json'}),
        new WebpackCleanup()
    ],

    module: {
        loaders: [
            {test: /\.jsx?$/, exclude: /node_modules/, loader: 'babel-loader'}
        ]
    },

    resolve: {
        modules: [ 'node_modules' ],
        extensions: ['.js', '.jsx']
    }
};
