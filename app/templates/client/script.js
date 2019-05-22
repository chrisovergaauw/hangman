function newGame() {
  $.ajax({
    type: "POST",
    dataType: 'json',
    url: "/hangman",
  }).done(function(data) {
    $('.hangman-word').text(data.hangman);
    $('.token').text(data.token);
    console.log(data.token)
  }).fail(function(data) {
    console.log(data)
  });
}

function guess(token, letter) {
  $.ajax({
    type: "PUT",
    dataType: 'json',
    contentType: 'application/json',
    url: "/hangman",
    data: JSON.stringify({ token: token, letter: letter}),
    beforeSend: function() {
      $(".letter").prop('disabled', true);
    }
  }).done(function(data, textStatus, xhr) {
    if (xhr.status == 304) {
      $('.letter').addClass("error");
      $('.letter').focus();
      return;
    }
    $('.hangman-word').text(data.hangman);
    $('.token').text(data.token);
    if (!data.correct) {
      failures = $('.wrong').length+1;
      drawHangman(failures);
    } else {
      if (data.hangman.indexOf("_") == -1) {
        getWordDefinition(data.hangman);
        $('.console').hide();
      }
    }
    cssClass = data.correct ? 'correct' : 'wrong';
    $('.attempts').append("<span class=" + cssClass +">"+letter+"</span>");
    $('.letter').focus();
  }).fail(function(data) {
    console.log(data)
  });
}

function getSolution(token) {
  $.ajax({
    type: "GET",
    dataType: 'json',
    url: "/hangman",
    data: { "token": token },
  }).done(function(data) {
    var hangman_word = $('.hangman-word').text();
    var solution = data.solution;

    for (var i = solution.length-1; i >= 0; i--) {
      if (hangman_word.charAt(i) != solution.charAt(i)) {
        error_string = "<span class='error'>"+ solution.charAt(i) + "</span>";
        updated_word = hangman_word
        hangman_word = updated_word.substr(0, i) + error_string + updated_word.substr(i+1);
      } else {
        if (hangman_word.indexOf("_") == -1) {
          $('.console').hide();
        }
      }
    }
    getWordDefinition(solution);
    $('.hangman-word').html(hangman_word);
  }).fail(function(data) {
    console.log(data)
  });
}

function drawHangman(failures){
  var canvas = $('#hangman-game')[0];
  var context = canvas.getContext("2d");
  context.strokeStyle = '#000000';

  switch (failures) {
    case 1: drawHead(context); break;
    case 2: drawBody(context); break;
    case 3: drawRightHand(context); break;
    case 4: drawLeftHand(context); break;
    case 5: drawRightFoot(context);
    case 6: drawLeftFoot(context);
    case 7: var token = $('.token').text();
      $('.console').toggle('scale');
      getSolution(token);
      hang(context);
  }
}

function getWordDefinition(word) {
  $.ajax({
    url: "http://api.wordnik.com:80/v4/word.json/"+word+"/definitions",
    data: { limit: 200, includeRelated: false, useCanonical: false, includeTags: false, api_key: 'd55b886c9abe00340b00d0c2add0c12cc6b6ee7084476d96c' },
    beforeSend: function() {
      $('.definition').html("<img height=50 src=spinner.gif></img>");
    }
  }).done(function(data) {
    $('.definition').text("");
    if (data.length > 0) {
      length = data.length > 2 ? 2 : data.length;
      for (var i = 0; i < length; i++) {
        $('.definition').text(data[i].text);
      }
    }
  }).fail(function() {
    $('.definition').text("");
    console.log("Unable to retrieve word definition from http://api.wordnik.com:80.");
  });
}

function hang(context) {
  // context.strokeStyle = '#da5754';
  drawHead(context);
  drawBody(context);
  drawRightHand(context);
  drawLeftHand(context);
  drawRightFoot(context);
  drawLeftFoot(context);
  drawFace(context);
}

function drawGallows(){
  var canvas = $('#hangman-game')[0];
  if (canvas == undefined) {
    return;
  }

  var context = canvas.getContext("2d");
  canvas.width = canvas.width;

  context.strokeStyle = '#000000';

  context.lineWidth = 20;
  context.beginPath();
  context.moveTo(350, 390);
  context.lineTo(10, 390);
  context.lineTo(70, 390);

  context.lineTo(70, 10);
  context.lineTo(200, 10);
  context.lineTo(200, 50);
  context.stroke();
}

function drawHead(context) {
  context.beginPath();
  context.arc(200, 100, 50, 0, Math.PI*2, false);
  context.closePath();
  context.lineWidth = 4;
  context.stroke();
}

function drawFace(context) {
  drawMouth(context);
  drawLeftEye(context);
  drawRightEye(context);
  drawLeftPupil(context);
  drawRightPupil(context);
  context.font = "26px Arial";
  context.strokeText("I can stand!", 255, 110);
}

function drawMouth(context) {
  context.beginPath();
  context.arc(210, 110, 20, 0, -Math.PI, false);
  context.closePath();
  context.lineWidth = 1;
  context.stroke();
}

function drawLeftEye(context) {
  context.beginPath();
  context.arc(200, 100, 8, 0, Math.PI*2, true);
  context.closePath();
  context.stroke();
}

function drawLeftPupil(context) {
  context.beginPath();
  context.arc(200, 105, 4, 0, Math.PI*2, true);
  context.closePath();
  context.fillStyle = "black";
  context.fill();
}

function drawRightPupil(context) {
  context.beginPath();
  context.arc(220, 105, 4, 0, Math.PI*2, true);
  context.closePath();
  context.fillStyle = "black";
  context.fill();
}

function drawRightEye(context) {
  context.beginPath();
  context.arc(220, 100, 8, 0, Math.PI*2, true);
  context.closePath();
  context.stroke();
}


function drawBody(context) {
  context.beginPath();
  context.moveTo(200, 150);
  context.lineTo(200, 300);
  context.stroke();
}

function drawRightHand(context) {
  context.beginPath();
  context.moveTo(200, 170);
  context.lineTo(150, 250);
  context.stroke();
}

function drawLeftHand(context) {
  context.beginPath();
  context.moveTo(200, 170);
  context.lineTo(250, 250);
  context.stroke();
}

function drawRightFoot(context) {
  context.beginPath();
  context.moveTo(200, 300);
  context.lineTo(150, 380);
  context.stroke();
}

function drawLeftFoot(context) {
  context.beginPath();
  context.moveTo(200, 300);
  context.lineTo(250, 380);
  context.stroke();
}

$(document).ready(function(){
  drawGallows();
  $('.console').hide();

  $(document).on('click', '#new-game', function(e){
    drawGallows();
    $('.attempts').empty();
    $('.definition').empty();

    newGame();
    $('.console').toggle('scale');
    $('.letter').focus();
  })

  $(document).on('click', '#guess', function(e){
    token = $('.token').text();
    letter = $('.letter').val();
    attempts = $('.attempts').text().toLowerCase();
    $('.letter').val('');
    $('.letter').focus();

    if (letter.trim().length < 1) {
      $('.letter').addClass("error");
      return;
    }
    $('.letter').removeClass("error");

    guess(token, letter);
    $(".letter").prop('disabled', false);
  })

  $(document).on('keypress', 'input.letter', function(e){
    var keycode = (e.keyCode ? e.keyCode : e.which);
    if(keycode == '13'){
      $('#guess').click();
    }
  })

  // var csrftoken = $('meta[name=csrf-token]').attr('content')
  var csrftoken = "{{ csrf_token() }}";

  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken)
        console.log('setting csrftoken...')
        console.log(csrftoken)
      }
    }
  });
});
