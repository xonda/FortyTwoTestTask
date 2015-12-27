$(document).ready(function(){

    var title = $('title').text();
    var last_number = 0;
    var new_count = 0;
    var priority_flag = false;
    var sort_flag = 0;
    var filter = $('#req-filter');
    var sort = $('#req-sort');

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
        if (sort_flag != 0){
            sortArray(data, 'fields.priority', sort_flag)
        }
        for (var i=0;i < data.length;i++) {
            if (priority_flag && data[i].fields.priority != '1') { continue; }
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
            content += '<td>' + data[i].fields.priority + '</td>';
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

    function sortArray(objArray, prop, direction){
        if (arguments.length<2) throw new Error("sortArray requires 2 arguments");
        var direct = arguments.length>2 ? arguments[2] : 1;

        if (objArray && objArray.constructor===Array){
            var propPath = (prop.constructor===Array) ? prop : prop.split(".");
            objArray.sort(function(a,b){
                for (var p in propPath){
                    if (a[propPath[p]] && b[propPath[p]]){
                        a = a[propPath[p]];
                        b = b[propPath[p]];
                    }
                }
                // convert numeric strings to integers
                a = a.match(/^\d+$/) ? +a : a;
                b = b.match(/^\d+$/) ? +b : b;
                return ( (a < b) ? -1*direct : ((a > b) ? 1*direct : 0) );
            });
        }
    }


    filter.click(function(){
        priority_flag = !priority_flag;
        filter.toggleClass('glow', 'addOrRemove');
        upd_requests();
    });

    sort.click(function(){
        switch (sort_flag) {
            case 0:
                sort_flag = 1;
                sort.addClass('glow');
                sort.prepend('<div class="arrow-up"></div>');
                break;
            case 1:
                sort_flag = -1;
                $('.arrow-up').remove();
                sort.prepend('<div class="arrow-down"></div>');
                break;
            case -1:
                sort_flag = 0;
                $('.arrow-down').remove();
                sort.removeClass('glow');
                break
        }
        console.log(sort_flag);
        upd_requests();
    });

    upd_requests();
    setInterval(upd_requests, 5000);

});
