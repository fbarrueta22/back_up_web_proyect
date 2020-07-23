function goToHome(){
  window.location = "/";
}

function goToJuegosPage(){
  window.location = "/juegos";
}

function goToResenasPage(){
  window.location = "/resenas";
}

function goToContactoPage(){
  window.location = "/contacto";
}

function goToSignUpPage(){
  window.location = "/signup";
}

function goToLoginPage(){
  window.location = "/login";
}

$(function() {
  $('#login-form-link').click(function(e) {
    $("#login-form").delay(100).fadeIn(100);
 		$("#register-form").fadeOut(100);
		$('#register-form-link').removeClass('active');
		$(this).addClass('active');
		e.preventDefault();
	});
	$('#register-form-link').click(function(e) {
		$("#register-form").delay(100).fadeIn(100);
 		$("#login-form").fadeOut(100);
		$('#login-form-link').removeClass('active');
		$(this).addClass('active');
		e.preventDefault();
	});
  $("#login-submit").click(function() {
    if($("#usernameLogin").val() != "" && $("#passwordLogin").val() != ""){
      var tmpObject = new Object();
      tmpObject.username = $("#usernameLogin").val();
      tmpObject.password = $("#passwordLogin").val();

      $.ajax({
          url : 'http://127.0.0.1:8080/authenticate',
          data : tmpObject,
          method : "POST", //en este caso
          dataType : 'json',
          success : function(response){
            window.location = "/";
          },
          error: function(error){
            alert(error.responseJSON['msg']);
          }
      });
    }else{
      alert('Falta completar datos');
      return;
    }
  });
  $("#register-submit").click(function() {
    if($("#usernameRegister").val() != "" && $("#nameRegister").val() != "" && $("#lastnameRegister").val() != "" && $("#passwordRegister").val() != ""){
      var tmpObject = new Object();
      tmpObject.username = $("#usernameRegister").val();
      tmpObject.password = $("#passwordRegister").val();
      tmpObject.name = $("#nameRegister").val();
      tmpObject.lastname = $("#lastnameRegister").val();

      $.ajax({
          url : 'http://127.0.0.1:8080/users',
          data : tmpObject,
          method : "POST", //en este caso
          dataType : 'json',
          success : function(response){
            var tmpObject2 = new Object();
            tmpObject2.username = tmpObject.username;
            tmpObject2.password = tmpObject.password;

            $.ajax({
                url : 'http://127.0.0.1:8080/authenticate',
                data : tmpObject2,
                method : "POST", //en este caso
                dataType : 'json',
                success : function(response){
                  window.location = "/";
                },
                error: function(error){
                  alert(error.responseJSON['msg']);
                }
            });

          },
          error: function(error){
            alert(error.responseJSON['msg']);
          }
      });
    }else{
      alert('Falta completar datos');
      return;
    }
  });
});
