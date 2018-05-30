var search_bar = document.getElementById("search_team");

search_bar.addEventListener("input", function() {
  $.ajax({
    url: "/find_teams?team_num=" + search_bar.value,
    success: function(result){
      update_collection(result);
    }
  });
});

var collection = document.getElementById("collection");

var update_collection = function(html) {
  collection.innerHTML = "";
  collection.innerHTML = html;
}
