$(document).ready(function(){

    $("#datepicker").datepicker({ dateFormat: 'yy-mm-dd' });

    function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#preview').attr('src', e.target.result).css({"width": "auto", "height": "auto"});
        };
        reader.readAsDataURL(input.files[0]);
        }
    }

    $("#id_photo").change(function(){
        readURL(this);
    });



    var cookieName = 'csrftoken';
    var xHeaderName = 'X-CSRFToken';

    var csrfSafeMethod = function (method) {
        return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
    };

    var getCookie = function (cookie) {
        var cookieValue = null;

        try {
            cookieValue = document.cookie.split(';')
                .map(function (x) {
                    return x.trim().split('=');
                })
                .filter(function (x) {
                    return x[0] == cookie;
                })
                .map(function (x) {
                    return x[1];
                })[0];
        } catch (e) {
            console.error(e);
        }
        return cookieValue;
    };

    $.csrfAjaxSupport = function () {
        $.ajaxSetup({
            crossDomain: false,
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    xhr.setRequestHeader(xHeaderName, getCookie(cookieName));
                }
            }
        });
    };


    var edit_info_options = {
    target:        '#ajaxwrapper',   // target element(s) to be updated with server response
    beforeSubmit:  beforeSubmit,  // pre-submit callback
    success:       submitSuccess  // post-submit callback
    };

    $('#edit_form').ajaxForm(edit_info_options);

    function beforeSubmit(formData, jqForm, options) {
          $('#ajaxwrapper').empty();
          $(":input").attr('disabled', true);
          $(".buttons_block").append('<span class="blink">Saving Info, please wait... </span>');
          setInterval(blinker, 500);
    return true;
    }

    function submitSuccess(responseText, statusText, xhr, $form)  {
        $(":input").attr('disabled', false)
        $(".blink").remove();
    }


    function blinker() {
    var blink = $('.blink');
    blink.fadeOut(500);
    blink.fadeIn(500);
}



});
