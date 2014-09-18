var socket = io('/echo');
socket.on('connect', function(){
  console.log('connected');
  socket.emit('message', 'hello world');
  socket.on('message', function(data){
      console.log(data)
  });
  socket.on('disconnect', function(){
      console.log('disconnected')
  })
});
