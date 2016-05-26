var targetContainer = document.getElementById("log-container");
var eventSource = new EventSource("/subscribe");

eventSource.onmessage=  function(e) {
    console.log(e);
    var newElement = document.createElement("li");

      newElement.innerHTML = "message: " + e.data;
      targetContainer.appendChild(newElement);

};
