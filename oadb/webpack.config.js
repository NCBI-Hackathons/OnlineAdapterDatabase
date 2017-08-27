var path = require("path");
var ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = {
    context: __dirname,

    entry: './react/entry',

    output: {
        path: path.resolve('./dist'),
        filename: "[name].bundle.js"
    },

    plugins: [
        new ExtractTextPlugin("[name].bundle.css")
    ],

    module: {
        loaders: [
            {
                test: /\.css$/,
                exclude: /node_modules/,
                loader: ExtractTextPlugin.extract("style-loader", "css-loader")
            },
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
