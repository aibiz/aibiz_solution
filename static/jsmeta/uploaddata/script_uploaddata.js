function showModal(){
    var file = document.getElementById('file');
    var extension = file.value.split('.').pop().toLowerCase();
    if(file.value == ''){
        file.focus();
        return false;
    }
    if(extension != 'zip'){
        file.focus();
        alert('zip파일을 올려주세요.');
        return false;
    }
    $('#directory-modal').modal('show');
}

function upload(){
    var directory_name = document.getElementById('directory-name');
    if(directory_name.value == ''){
        directory_name.focus();
        return false;
    }

    var url = $("#UploadForm").attr("action");
    var form = $('#UploadForm')[0]; 
    var formData = new FormData(form);
    formData.append('directory-name', directory_name.value);

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