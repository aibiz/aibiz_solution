function register(){
    var id = document.getElementById('card-id').value;
    var password = document.getElementById('card-password').value;
    var password_confirm = document.getElementById('card-confirm-password').value;
    var name = document.getElementById('card-name').value;
    var email = document.getElementById('card-email').value;
    var checkbox = document.getElementById('card-register-checkbox').checked;

    if(!checkbox){
        document.getElementById('card-register-checkbox').focus();
        alert('약관동의를 해주세요.');
        return false;
    }
    if(id == ''){
        document.getElementById('card-id').focus();
        return false;
    }
    else{
        if(!CheckID(id)){
            document.getElementById('card-id').focus();
            return false;
        }
    }
    if(password == ''){
        document.getElementById('card-password').focus();
        return false;
    }
    else{
        if(!CheckPassword(password)){
            document.getElementById('card-password').focus();
            return false;
        }
    }
    if(password_confirm == ''){
        document.getElementById('card-confirm-password').focus();
        return false;
    }
    else{
        if(!SamePassword()){
            document.getElementById('card-confirm-password').focus();
            return false;
        }
    }
    if(name == ''){
        document.getElementById('card-name').focus();
        return false;
    }
    if(email == ''){
        document.getElementById('card-email').focus();
        return false;
    }
    else{
        if(!CheckEmail(email)){
            document.getElementById('card-email').focus();
            return false;
        }
    }
    if(checkbox == ''){
        document.getElementById('card-register-checkbox').focus();
        return false;
    }

    var url = $("#RegisterForm").attr("action");
    console.log(url);
    var form = $('#RegisterForm')[0]; 
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
                alert(result.message);
                location.href='/login'
            }
        }
    });
}

//아이디 정규식
function CheckID(str){
    if(str == '')
        return;
    var reg_id = /^[a-z]+[a-z0-9]{5,19}$/g;

    if( !reg_id.test(str)) {
        document.getElementById('idError').innerText = '아이디는 영문자로 시작하는 6~20자 영문자 또는 숫자이어야 합니다.';
        return false;
    }
    else{
        document.getElementById('idError').innerText = ''
        return true;
    }
}

//이메일 정규식
function CheckEmail(str){                                        
     var reg_email = /^([0-9a-zA-Z_\.-]+)@([0-9a-zA-Z_-]+)(\.[0-9a-zA-Z_-]+){1,2}$/;

     if(!reg_email.test(str)){
        document.getElementById('emailError').innerText = '잘못된 이메일 형식입니다.';
        return false;
    }         
     else{
        document.getElementById('emailError').innerText = ''
        return true;
    }             
}

//비밀번호 정규식
function CheckPassword(str){
    if(!/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d~!@#$%^&*()+|=]{8,16}$/.test(str)){
        document.getElementById('passwordError').innerText = '숫자와 영문자 조합으로 8~16자리를 사용해야 합니다.';
        return false;
    }
  
    var checkNum = str.search(/[0-9]/g); // 숫자사용
    var checkEng = str.search(/[a-z]/ig); // 영문사용
  
    if(checkNum <0 || checkEng <0){
        document.getElementById('passwordError').innerText="숫자와 영문자를 조합하여야 합니다.";
        return false;
    }
    else{
        document.getElementById('passwordError').innerText="";
        return true;
    }
}
//비밀번호 일치 확인
function SamePassword(){
    var password = document.getElementById('card-password').value;
    var password_confirm = document.getElementById('card-confirm-password').value;
    if(password== '' || password_confirm =='')
        return
    if(password != password_confirm){
        document.getElementById('passwordError').innerText="비밀번호가 일치하지 않습니다.";
        return false;
    }
    else{
        document.getElementById('passwordError').innerText="";
        return true;
    }
}