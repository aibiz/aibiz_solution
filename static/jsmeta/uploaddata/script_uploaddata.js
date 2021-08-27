function upload(){
    var file = document.getElementById('file');
    if(file.value == ''){
        file.focus();
        return false;
    }
    var url = $("#UploadForm").attr("action");
    var form = $('#UploadForm')[0]; 
    var formData = new FormData(form);
    $.ajax({
        type : 'POST',
        url : url,
        headers: { "X-CSRFToken": csrftoken },
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
                alert(result.message);
                location.reload(true);
            }
        }
    });
}