var socket = io('/echo');
socket.on('connect', function(){
  console.log('connected');
  socket.on('message', function(data){
      console.log(data);
      $('#messages').append(data);
  });
  socket.on('disconnect', function(){
      console.log('disconnected')
  })
});

