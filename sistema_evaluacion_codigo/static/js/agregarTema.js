$(document).ready(function() {
    $('#agregar_tema').on('submit', function(event){
        event.preventDefault();
        console.log("probando");
        agregar_tema();

    });
    function agregar_tema() {
        console.log("Agregando el tema") // sanity check
        $.ajax({
            url : "{% url 'agregar_tema' %}", // the endpoint
            type : "POST", // http method
            data : { tema : $('#tema').val() , csrfmiddlewaretoken: '{{ csrf_token }}'}, // data sent with the post request
            dataType: 'json',

            // handle a successful response
            success : function(json) {
                $('#temas').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console
                console.log(json.tema_id);
                console.log("success"); // another sanity check
                $('#temas').append($('<option>', {
                    value: json.tema_id,
                    text: json.tema
                }));
                $('.modal').modal('hide');
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };

});
