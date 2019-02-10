$(document).ready(function() {
    $('.btnAdd').click(function(){
        var id_ejercicio = $(this).attr('id')
        var ejercicio = $('<li/>', {
          'html' : '<input type="number" name="puntajes[]" placeholder="Puntaje" min="1" max="100" required> <input type="hidden" name="ejercicios[]" value='+id_ejercicio+'> <spa class="text">' + $(this).attr('value') + '</spa> </input> <div  class="tools"> <i class="fa fa-trash-o remove_button" id="remove_button"> </i></div>',
          'id' : id_ejercicio,
          'class':'remove'
        });
        $('#field_wrapper').append(ejercicio);

    });

    $('#field_wrapper').on('click', '#remove_button', function(e){ //cuando se da clic al icono de eliminar
        e.preventDefault();
        $(this).parents('.remove').remove(); //Remueve el campo del html

    });

});

