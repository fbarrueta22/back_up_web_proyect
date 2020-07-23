function verifyUserLogged(){
  $.getJSON('/current_user', function(data){
      document.getElementById("btnLogout").style.display = "block";
      document.getElementById("btnSignUp").style.display = "none";
      document.getElementById("btnLogin").style.display = "none";
      $('#lblTitle').text("Bienvenido " + data['current']['name'] + " " + data['current']['lastname']);
    });
}



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

function logout(){
  $.getJSON('/logout', function(data){
    alert(data['msg']);
    window.location = "/";
  });
}

function goToSignUpPage(){
  window.location = "/signup";
}

function goToLoginPage(){
  window.location = "/login";
}
