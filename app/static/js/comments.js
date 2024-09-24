$(document).ready(function (){
    $('#sendComment').click(function (){
        var btn = $(this);
        $.ajax(btn.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'comment': $('#comment').val(),
            },
            'success': function (response){
               var comments = document.getElementById('comments');
               comments.innerHTML =comments.innerHTML + `<p>${$('#comment').val()}</p>`;
               $('#comment').val('');
            }
        });
    });

    $('.btnDelete').click(function (){
        var del_btn = $(this);
            $.ajax(del_btn.data('url'),{
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'success': function (response){
                document.getElementById(String(response.id)).outerHTML = '';
            }
        });
    });

        $('.btnUpdate').click(function (){
        var btn = $(this);
            $.ajax(btn.data('url'),{
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'success': function (response){
                var id=btn.data('id')
                var comments = document.getElementById('comments');
                var update_button = document.getElementById(String(response.id));
                comments.innerHTML = comments.innerHTML + id + "." +` <input id="${btn.data('id')}" type="text"><button></button><p></p>`
            }
        });
    });
});