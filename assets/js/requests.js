$(document).ready(function(){

    var title = $('title').text();
    var last_number = 0;
    var new_count = 0;

    function upd_requests() {
        $.ajax({
            url: '/upd_requests',
            dataType: "json"
        })
            .done(function(data){
                update_table(data);
                last_number = data[0].pk;
            });
    }

    function update_table(data){
        var content = '';
        var table_body = $('tbody');
        for (var i=0;i < data.length;i++) {
            content += '<tr>';
            content += '<td>' + data[i].pk + '</td>';
            content += '<td>' + data[i].fields.time + '</td>';
            content += '<td>' + data[i].fields.host + '</td>';
            content += '<td>' + data[i].fields.path + '</td>';
            content += '<td>' + data[i].fields.method + '</td>';
            content += '<td>' + data[i].fields.user_agent + '</td>';
            content += '<td>' + data[i].fields.get + '</td>';
            content += '<td>' + data[i].fields.post + '</td>';
            content += '<td>' + data[i].fields.is_secure + '</td>';
            content += '<td>' + data[i].fields.is_ajax + '</td>';
            content += '<td>' + data[i].fields.user + '</td>';
            content += '<td> 1 </td>';
            content += '</tr>';
        }
        table_body.html(content);
        $('#reqTable').removeClass('hidden');


        if (document.hidden) {
            if (last_number < data[0].pk && last_number != 0) {
                new_count += data[0].pk - last_number;
                $('title').text('(' + new_count + ') ' + title);
            }
        }

    }

    $(window).focus(function(){
        $('title').text(title);
        new_count = 0
    });

    upd_requests();
    setInterval(upd_requests, 5000);

});
