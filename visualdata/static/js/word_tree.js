google.charts.load('current', {packages:['wordtree']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {

    $.ajax({
        url: '/api/wordtree/' + user + '/', 
        success: function(data) {
          var data = google.visualization.arrayToDataTable(data);
          var options = {
            wordtree: {
              format: 'implicit',
              word: 'cats'
            }
          };
          var chart = new google.visualization.WordTree(document.getElementById('wordtree_basic'));
          chart.draw(data, options);      
        }
    });
}