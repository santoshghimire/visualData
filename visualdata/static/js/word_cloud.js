$(document).ready(function() {
    get_wordcloud();
});

function get_wordcloud() {
    var url = '/api/wordcloud/' + user + '/';
    $.ajax({
        url: url, 
        success: function(data) {
            $('#keywords').jQCloud(data, {
              width: 800,
              height: 550
            });
        }
    });
}
