
$(function(){
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            
            if (localStorage.getItem('token')) {
                xhr.setRequestHeader("Authorization", "JWT " + localStorage.getItem('token'));
            }

            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                var csrftoken = getCookie('csrftoken');
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });  

    toastr.options = {
        progressBar: true,
        timeOut: 7000
    }

    function reloadAfter(timeOut){
        setTimeout(function(){
            location.reload();
        }, timeOut);
    };

    $(".payment_button").on("click", function(){
        id = $(this).parent().siblings().first().children().first().val()
        payment_value = $(this).parent().siblings().eq(5).text()
        $("#id_user").val(id)
        $("#payment_value").val(payment_value)
        $(".bd-modal-sm").modal("show")
    })

    $("#payment_submit").on("click", function(){
        id = $("#id_user").val()
        payment_value = $("#payment_value").val()

        if(payment_value){
            $.ajax({
                type: 'POST',
                url: '/user_payment/'+ id +'/',
                data: {"payment_value":payment_value},
                dataType: 'json'
                }).done(function(data){ 
                    if(data["success"]){
                        toastr.success("pago com sucesso")
                        reloadAfter(1000)
                    }      
                    else{
                        toastr.error(data["message"])                
                    }          
                })
                .fail(function(jq, textStatus, error){
                    toastr.error("Não foi possivel realizar essa operação");
                });                                                            
            
        }else{
            toastr.error("Não foi possivel realizar essa operação");
        }
    });  
    
    
    
});
