var targetContainer = document.getElementById("log-container");
var eventSource = new EventSource("/subscribe");

eventSource.onmessage=  function(e) {
    console.log(e);
    var newElement = document.createElement("li");

      newElement.innerHTML = "message: " + e.data;
      targetContainer.appendChild(newElement);

};


var data = [
  { label: 'Layer 1', values: [ {x: 0, y: 0}, {x: 1, y: 1}, {x: 2, y: 2} ] },
  { label: 'Layer 2', values: [ {x: 0, y: 0}, {x: 1, y: 1}, {x: 2, y: 4} ] }
];

var areaChartInstance = $('#area').epoch({
    type: 'area',
    data: data,
    axes: ['left', 'right', 'bottom']
});
