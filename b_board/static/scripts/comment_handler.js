/*
клик на кнопках "принять" или "отклонить" посылает POST запрос с коммандой
"accept-PK" или "reject-PK". На сервере, соответственно, или комментарию
присвается статус "принят" или комментарий удаляетя. Но фронтэнде
или появляется написть "принят" вместо кнопок, или скрывается див с комментарием
*/
    
$('.btn-accept').click(function(e){
    var pk = $(this).attr('comment-pk');
    $.ajax({
        type: "POST",
        url: $(this).attr('data-url'),
        data: {'csrfmiddlewaretoken':  $(this).attr('token'),
               'pk': pk,
            },
        // получаем подтверждение сервера и меняем фронтэнд
        success:function (data) {
            if(data = 'success'){
                $('#advert_author_buttons_' + pk).hide();
                $('#advert_comment_success_' + pk).css("display", "block");
            };
        },
    });
});
    
$('.btn-delete').click(function(e){
    var pk = $(this).attr('comment-pk');
    $.ajax({
        type: "POST",
        url: $(this).attr('data-url'),
        data: {'csrfmiddlewaretoken':  $(this).attr('token'),
               'pk': pk,
            },
        // получаем подтверждение сервера и меняем фронтэнд
        success:function (data) {
            if(data = 'success'){
                $('#comment_div_' + pk).hide();
            };
        },
    });
});

/*
клик на кнопках "изменить" или "добавить" запрашивает с сервера заполненную
или пустую форму. Формы обрабатываются в соответствующих функциях,
страница обновляется и перематывается на соответствующий комментарий
*/

$('.btn-edit').click(function(e){
    var pk = $(this).attr('comment-pk');
    $.ajax({
        url: $(this).attr('data-url'),
        data: {
               'pk': pk,
            },
        // получаем подтверждение сервера и меняем фронтэнд
        success:function (data) {
            $('#form-div').html(data);
            $('#form-area').css("display", "block");
        },
    });
});

$('.btn-add').click(function(e){
    $.ajax({
        url: $(this).attr('data-url'),
        data: {
               'advert': $(this).attr('advert-pk'),
            },
        // получаем подтверждение сервера и меняем фронтэнд
        success:function (data) {
            $('#form-div').html(data);
            $('#form-area').css("display", "block");
        },
    });
});

/*
закрываем блок с формой по кнопке "закрыть" или "submit"
*/

$('#form-area').submit(function(event){
    $('#form-area').css("display", "none")
});

$('#close-form-btn').click(function(event){
    $('#form-area').css("display", "none");
});



