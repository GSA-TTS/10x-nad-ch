const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
  mode: "development",
  entry: {
    main: [
      "./src/index.ts", // Path to your main JavaScript or TypeScript file
      "./sass/index.scss", // Path to your SASS entry file
    ],
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: "ts-loader",
        exclude: /node_modules/,
      },
      {
        test: /\.s[ac]ss$/i,
        use: [
          { loader: MiniCssExtractPlugin.loader },
          { loader: "css-loader", options: { url: false, sourceMap: true } },
          {
            loader: "postcss-loader",
            options: {
              sourceMap: true,
            },
          },
          {
            loader: "sass-loader",
            options: {
              implementation: require("node-sass"),
              sourceMap: true,
              sassOptions: {
                includePaths: [
                  path.resolve(__dirname, "node_modules"),
                  path.resolve(__dirname, "node_modules/uswds/dist/scss"),
                  path.resolve(__dirname, "node_modules/uswds/dist/fonts"),
                ],
              },
            },
          },
        ],
      },
      {
        test: /\.css$/,
        include: [path.resolve(__dirname, "node_modules/@uswds/uswds")],
        use: [MiniCssExtractPlugin.loader, "css-loader"],
      },
    ],
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: "style.css",
    }),
  ],
  resolve: {
    extensions: [".tsx", ".ts", ".js", ".scss"],
    alias: {
      uswds: path.resolve(__dirname, "node_modules/@uswds/uswds"),
    },
  },
  output: {
    filename: "bundle.js",
    path: path.resolve(__dirname, "dist"),
  },
};
