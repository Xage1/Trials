const { watch } = require("fs");
const path = require("path");
const HtmlWebpackPlugin = require('html-webpack-plugin');
const { title } = require("process");
const { Module } = require("module");

module.exports = {
    mode: "development",
    entry:{
        main:path.resolve(__dirname, "src/index.js"),
    },
    output:{
        path:path.resolve(__dirname, "dest"),
        filename:"[name].js",
    },
    devServer: {
        static:{
            directory: path.resolve(__dirname, "dest"),
            watch: true,
        },
    },
    module: {
        rules:[
            {
            test: /\.css$/,
            use: ["style-loader", "css-loader"]
            },
        ],
    },
    plugins: [
        new HtmlWebpackPlugin({
            title: "News of the World",
            filename: "index.html",
            template: "src/template.html",
            inject: "body"
        }),
    ],
};
