var all_button = document.getElementById("select_all");
var none_button = document.getElementById("select_none");
var checkboxes = document.getElementsByName("teams");

all_button.addEventListener("click", function() {
  for (var i = 0; i < checkboxes.length; i++) {
    checkboxes[i].checked = true;
  }
});

none_button.addEventListener("click", function() {
  for (var i = 0; i < checkboxes.length; i++) {
    checkboxes[i].checked = false;
  }
});
