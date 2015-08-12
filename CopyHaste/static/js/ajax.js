function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min)) + min;
}

$.ajax({url: 'https://api.github.com/search/repositories?q=language:python+sort:updated'}).done(function(data) {
  var l = data.items.length;
  var i = getRandomInt(0, l - 1);
  var item = data.items[i];
  var repo = item.name;
  var user = item.owner.login;

  $.ajax({url: 'https://api.github.com/search/code?q=language:python+repo:' + item.full_name}).done(function(codeData) {
    var cl = codeData.items.length;
    var ci = getRandomInt(0, cl - 1);
    var citem = codeData.items[ci];
    var path = citem.path;
    console.log("stuff to pass to python");
    console.log("user: " + user);
    console.log("repo: " + repo);
    console.log("file: " + path);
  });

});
