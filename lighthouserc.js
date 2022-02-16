module.exports = {
  ci: {
    collect: {
      staticDistDir: 'output/',
      url: ["http://localhost/index.html", "http://localhost/about.html", "http://localhost/authors.html", "http://localhost/search.thml", "http://localhost/ipfs.html"],
    },
    upload: {
      target: 'temporary-public-storage',
    },
  },
};
