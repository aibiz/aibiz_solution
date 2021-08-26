function login(){
    var id = document.getElementById('card-id').value;
    var password = document.getElementById('card-password').value;

    if(id == ''){
        document.getElementById('card-id').focus();
        return false;
    }
    if(password == ''){
        document.getElementById('card-password').focus();
        return false;
    }

    var url = $("#LoginForm").attr("action");
    var form = $('#LoginForm')[0]; 
    var formData = new FormData(form);
    $.ajax({
        type : 'POST',
        url : url,
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        data : formData,
        cache: false,
        contentType: false,
        processData: false,
        error: function(request,status,error){
             alert("code:"+request.status+"\n"+"error:"+error);
        },
        success : function(result){
            if (result.success == false) {
                    alert(result.message);
            }
            else {
                location.href='/'
            }
        }
    });
}

function enterkey() {
    if (window.event.keyCode == 13) {
        login();
    }
}