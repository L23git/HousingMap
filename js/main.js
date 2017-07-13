// Listen for form submit
document.getElementById('myform').addEventListener('submit', saveBookmark);

function saveBookmark(e){
  // Get form values
  var siteName = document.getElementById('siteName').value;
  var siteUrl = document.getElementById('siteUrl').value;
  if(!siteName || !siteUrl){
    alert("Please fill out the form");
    return false;
  }
  var bookmark = {
    name: siteName,
    url: siteUrl
  }

  /*
  localStorage.setItem('test', 'Hello World')
  console.log(localStorage.getItem('test'))
  localStorage.setItem('test')
  console.log(localStorage.getItem('test'))
  */

  if(localStorage.getItem('bookmarks') === null){
    var bookmarks = [];
    //Add to arrray
    bookmarks.push(bookmarks);
    // set to local storage
    localStorage.setItem('bookmarks', JSON.stringify(bookmarks));
  }
  else({
    // get bookmarks from local storage
    var bookmarks = JSON.parse(localStorage.getItem('bookmarks'));
    // Add the bookmark were submitting to the arrray
    bookmarks.push(bookmakrs);
    // Set back to local storage
    localStorage.setItem('bookmarks', JSON.stringify(bookmarks));
  })
  // Refetch bookmarks
  fetchBookmarks();
  e.preventDefault();
}

function deleteBookmark(url){
  // Get bookmarks from localStorage
  var bookmarks = JSON.parse(localStorage.getItem('bookmarks'))
  for(var i =0; i < bookmarks.length; i++){
    if(bookmarks[i].url == url){
      //Remove from arrray
      bookmarks.splice(i,1);
    }
  }
  localStorage.setItem('bookmarks', JSON.stringify(bookmarks));

  // Refetch bookmarks
  fetchBookmarks();
}
function fetchBookmarks(){
  var bookmarks = JSON.parse(localStorage.getItem('bookmarks'));
  // Get output id
  var bookmarkResults = document.getItemById('bookmarkResults');

  //build ooutput
  bookmarkResults.innerHTML = "";
  for(var i = 0; i < bookmakrs.length; i++){
    var name = bookmarks[i].name;
    var url = bookmarks[i].url;

    bookmarkResults.innerHTML += '<div class="well>'+
                                  '<h3>'+name+
                                  '<a class="btn btn-default" target="_blank"'+
                                  'visit'+'</a>'+
                                  '<a onclick="deleteBookmarks(\'+urlclass="btn btn-danger" href="bookmarks"'+
                                  'Delete'+'</a>'+
                                  '/<h3>'+
                                  '</div>';
  }
}
