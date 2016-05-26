var targetContainer = document.getElementById("log-container");
var eventSource = new EventSource("/subscribe");

var data = [
    {
    label: "One",
    values: []
    },
    {
    label: "Two",
    values: []
    },
];

var chart = $('#area').epoch({
    type: 'time.line',
    data: data,
    axes: ['left', 'right', 'bottom'],
    queueSize: 1,
    historySize: 1,
    fps: 60
});

eventSource.onmessage = function(e) {
    console.log(e);
    var newElement = document.createElement("li");

      var newData = [
          {time: Date.now(), y: e.data},
          {time: Date.now(), y: e.data * 3}
      ];

      chart.push(newData);
};
