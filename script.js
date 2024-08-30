// Example script to handle dynamic interest selection, not needed if using checkboxes
function addInterest() {
    var interest = document.getElementById("interest_input").value;
    var list = document.getElementById("interest_list");
    var entry = document.createElement('li');
    entry.appendChild(document.createTextNode(interest));
    list.appendChild(entry);
    document.getElementById("interest_input").value = "";
}
