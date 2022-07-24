module.exports = {
  ci: {
    collect: {
      staticDistDir: 'output/',
      url: ["http://localhost/index.html", "http://localhost/latest.html", "http://localhost/search.html", "http://localhost/ipfs.html"],
    },
    upload: {
      target: 'filesystem',
    },
  },
};