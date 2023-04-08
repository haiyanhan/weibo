// Get references to the buttons and the table
var queryButton = document.getElementById("query-btn");
var addButton = document.getElementById("add-btn");
var editButton = document.getElementById("edit-btn");
var deleteButton = document.getElementById("delete-btn");
var dataTable = document.getElementById("data-container");

// Add event listeners to the buttons
queryButton.addEventListener("click", queryDatabase);
addButton.addEventListener("click", addRecord);
editButton.addEventListener("click", editRecord);
deleteButton.addEventListener("click", deleteRecord);

function addRecord() {
    // Prompt the user for input and create a new data row
    var newRow = "<tr><td>new ID</td><td>new username</td>...</tr>";
    dataTable.innerHTML += newRow;
  }
function deleteRecord() {
    var selectedRow = dataTable.querySelector("tr.selected");
    selectedRow.remove();
  }
function editRecord() {
    var selectedRow = dataTable.querySelector("tr.selected");
    selectedRow.innerHTML = "<td>new ID</td><td>new username</td>...";
  }
function queryDatabase() {
    // Send an AJAX request异步请求 to the server-side code that queries the database
    $.ajax({
      url: "/query",
      method: "POST",
      data: { /* ... any data needed for the query ... */ },
      success: function(response) {
        // Convert the JSON data to an array of objects
        var data = JSON.parse(response);
        updateTable(data);
      }
    });
  }
function updateTable(data) {
    // Clear the existing rows from the table
    dataTable.innerHTML = "<tr><th>ID</th><th>...</th></tr>";
    // Add each row to the table
    for (var i = 0; i < data.length; i++) {
      // Create a new row and set the data values
      var newRow = "<tr>" +
                   "<td>" + data[i].id + "</td>" +
                   "<td>" + data[i].username + "</td>" +
                   "..." +
                   "</tr>";
      // Add the new row to the table
      dataTable.innerHTML += newRow;
    }
  }