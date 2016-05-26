var eventSource = new EventSource("/subscribe");

var series1 = new TimeSeries();

eventSource.onmessage = function(e) {
    console.log(e);

    series1.append(new Date().getTime(), e.data);
};

 function createTimeline() {
   var chart = new SmoothieChart({
       maxValueScale: 1.5,
       grid:{
           fillStyle: '#ffffff'
       },
       labels:{
           fillStyle: '#000000'
       }
   });
   chart.addTimeSeries(series1, { strokeStyle: 'rgba(255, 0, 0, 1)', lineWidth: 2 });
   chart.streamTo(document.getElementById("smoothie"), 50);
}

createTimeline();
