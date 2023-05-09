/*\
скрипт подгрузки блока объявлений на главную страницу
получаемый блок содержит кнопку вызова следующего блока 
на dive, содержащем кнопке висит аттрибут "last-date" через который передается
дата и время последнего показанного в блоке объявления для поиска следующего
*/

//функция получения блока объявлений черзе ajax запрос
function get_adverts(get_btn){
    // если функция вызвана кнопкой показываем спиннер
    // и устанавливаем дату последнего объявления
    if(get_btn != null){
        var last_date = get_btn.attr('last-date');
        get_btn.hide();
        $('#spinner').show();
    } else {
        var last_date = null;
    };

    // запрашиваем блок начиная с последней даты
    // url и Id категории берем из аттрибутов блока "#adverts"
    $.ajax({
        url: $("#adverts").attr("data-urls"),
        data: {
                'last_date': last_date,
                'category': $("#adverts").attr("data-category"),
                },
        success: function (data) {
            $("#adverts").append(data);
            if(get_btn != null){
                //чуток прокручиваем страницу что бы поднять появившийся блок объявлений
                $('html').animate({ 
                        scrollTop: $(window).scrollTop()+$(window).height()/2
                    }, 100 // скорость прокрутки
                );
                $('#spinner').hide();
            };
        }
    });        
};

//привязка обработчика к динамически создаваемой кнопке
//вызов первого блока объявлений
$(document).ready(function() {
    get_adverts(null);
    $('#spinner').hide();
    $('#adverts').on('click', '#btn', function() {
        var btn = $(this); 
        get_adverts(btn);
    });
});

