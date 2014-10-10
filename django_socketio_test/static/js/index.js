var socket = io.connect('/echo');
socket.on('connect', function(){
  console.log('connected');
  socket.on('message', function(data){
      console.log(data);
      $('#messages').append($('<p>').text(data));
  });
  socket.on('disconnect', function(){
      console.log('disconnected')
  })
});

Mousetrap.bind('ctrl+enter', function(e){
    var input_field = $('#input');
    var text = input_field.val();
  if(text.length > 0){
    socket.emit('message', text);
    input_field.val('');

    var blob = new Blob(['123', 'what', 'the', 'hell'])
    socket.emit('message', blob)
  }
  return false;
});
