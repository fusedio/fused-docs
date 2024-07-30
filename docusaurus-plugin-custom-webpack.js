// docusaurus-plugin-custom-webpack.js
module.exports = function (context, options) {
  return {
    name: "docusaurus-plugin-custom-webpack",
    configureWebpack(config, isServer, utils) {
      return {
        module: {
          rules: [
            {
              test: /\.py$/,
              type: "asset/source",
            },
          ],
        },
      };
    },
  };
};
