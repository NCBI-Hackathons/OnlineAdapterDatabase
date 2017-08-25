var path = require("path");
var BundleTracker = require('webpack-bundle-tracker');
var WebpackCleanup = require('webpack-cleanup-plugin');

module.exports = {
    context: __dirname,

    entry: './react/js/index',

    output: {
        path: path.resolve('./react/bundles'),
        filename: "[name].bundle.js"
    },

    plugins: [
        new BundleTracker({filename: './webpack-stats.json'}),
        new WebpackCleanup()
    ],

    module: {
        loaders: [
            {
                test: /\.jsx?$/,
                exclude: /node_modules/,
                loader: 'babel-loader',
                options: {
                    presets: [
                        'react',
                        'es2015'
                    ]
                }
            }
        ],
    },

    resolve: {
        modules: [ 'node_modules' ],
        extensions: ['.js', '.jsx']
    }
};
