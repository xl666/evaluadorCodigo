$(document).ready(function() {

    var casoDePrueba = '<div class="remove"><div class="form-group col-md-6"> <label for="id_nrc" class="control-label  requiredField">Entrada<span class="asteriskField">*</span></label> <div class="controls "> <textarea class="form-control" rows="5" name="entradas[]" required></textarea></div></div> <div class="form-group col-md-6"> <label for="id_nrc" class="control-label  requiredField">Salida<span class="asteriskField">*</span><a href="javascript:void(0);"  id="remove_button" class="deletelink remove_button"></a></label> <div class="controls "> <textarea class="form-control" name="salidas[]" rows="5" required></textarea></div></div>';
    $('#btnAdd').click(function(){
        $('#field_wrapper').append(casoDePrueba); // Add field html

    });

     $('#field_wrapper').on('click', '#remove_button', function(e){ //Once remove button is clicked
        e.preventDefault();
        $(this).parents('.remove').remove(); //Remove field html
    });

});


