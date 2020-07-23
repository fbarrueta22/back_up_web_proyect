let username;
let name;
function verifyUserLogged(){
  $.getJSON('/current_user', function(data){
      document.getElementById("btnLogout").style.display = "block";
      document.getElementById("btnSignUp").style.display = "none";
      document.getElementById("btnLogin").style.display = "none";
      $('#lblTitle').text("Bienvenido " + data['current']['name'] + " " + data['current']['lastname']);
      username = data['current']['username'];
    });
}

/*function get_all_games(){
  verifyUserLogged();
  $.getJSON("/games",function (data){
    var i=0;
    $.each(data, function(){
      template = '<div class="alert alert-success" role="alert" onclick="get_reviews(game_id)"><span>title</span></div>';
      template = template.replace('title',data[i]['title']);
      template = template.replace('game_id', data[i]['id']);
      $("#games").append(template);
      i=i+1;
    });
  });
}*/

function get_all_games(){
  verifyUserLogged();
  $.getJSON("/games",function (data){
    var i=0;
    $.each(data, function(){
      template = '<div class="alert alert-success" role="alert" onclick="get_reviews(game_id)"><span>name</span></div>';
      template = template.replace('name',data[i]['title']);
      template = template.replace('game_id', data[i]['id']);
      console.log(template);
      $("#games").append(template);
      i=i+1;
    });
  });
}




function get_reviews(game_id){
  
    $("#reviews").empty();

  $.getJSON("/get_reviews/"+game_id, function(data){
    let i=0;
    $.each(data,function(){
      let content; let valoration; let user_; let date;
      content=data[i]['content'];
      valoration=data[i]['valoration'];
      user_=data[i]['user'];
      date = data[i]['write_on'];
      template=template.replace('content',data[i]['content']);
      template=template.replace('user_id',data[i]['user_id']);
      template='<div class="comment-main-level">'+'<div class="comment-avatar"><img src="/static/images/descarga.png" alt=""></div>'+
      '<div class="comment-box">'+
        '<div class="comment-head">'+
          '<h6 class="comment-name by-author">'+user_+'</h6>'+
          '<span>'+date+'</span>'+
          '<i class="fa fa-reply"></i>'+
          '<i class="fa fa-heart"></i>'+
        '</div>'+
        '<div class="comment-content">'+
          '<p>Valoration: '+valoration+'%</p>'+
          '<p>'+content+'</p>'+
        '</div>'+
      '</div>'+
    '</div>';
      console.log(template);
      $("#reviews").append(template);
      i=i+1;
    });
  }); 

  $("#send").empty();
      let inputBox = '<form class=""> ' + 
      '<table>'+
        '<td>'+
          '<label for="content" style="color:white;">       Write a comment</label>'+
          '<div ><input id="content" style="width: 500px;height: 50px;" type="text" name="content"></div>' +
          '<label for="valoration" style="color:white;">    Put valoration</label>'+
          '<div><input id="valoration" style="width: 500px;height: 50px;" type="number" name="valoration"> </div>' +
        '</td>'+
        '<td>'+
          '<div><button type="button" class="btn btn-primary" onclick="send_comment(game_id,game_title)">Send</button></div>'+
        '</td>'+
      '</table>' + 
      '</form>';
      inputBox = inputBox.replace('game_id',game_id);
      inputBox = inputBox.replace('game_title',game_title);
      $("#send").append(inputBox);
}

function send_comment(game_id,game_title){
    var content = $('#content').val();
    var valoration = $('#valoration').val();
    console.log(username)
    var review = JSON.stringify({
        'valoration':valoration,
        'content':content,
        'user':username,
        'game':game_title
    });
    $.post({
        url : '/reviews',
        type : 'POST',
        dataType : 'json',
        contentType : 'application/json',
        data : review
    });
    get_reviews(game_id);
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
