google.charts.load('current', {packages:['wordtree']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {

    $.ajax({
        url: '/api/word/' + user + '/', 
        success: function(data) {
          var word_tree = google.visualization.arrayToDataTable(data.word_tree);
          var options = {
            wordtree: {
              format: 'implicit',
              // type: 'double'
              // word: data.word_tree[1][0].split(' ')[0]
            }
          };
          var chart = new google.visualization.WordTree(document.getElementById('wordtree_basic'));
          chart.draw(word_tree, options);


          $('#keywords').jQCloud(data.word_cloud, {
              width: 800,
              height: 550
          });
        }
    });
}