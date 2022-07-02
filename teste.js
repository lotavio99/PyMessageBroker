let net = require('net');

let host = 'localhost';
let port = 53;

let socket = new net.Socket();

socket.connect(port, host, () => {

    socket.write("sub teste");
    socket.write("teste");
//    socket.write(`MAIL FROM: <${from}>\n`);
//    socket.write(`RCPT TO: <${to}>\n`);
//    socket.write("DATA\n");
//    socket.write(`From:${name}\n`);
//    socket.write(`Subject:${subject}\n`);
//    socket.write(`${body}`);
//    socket.write("\r\n.\r\n");
//    socket.write("QUIT\n");
});

socket.on('data', data => {
  console.log(`${data}`);
});

socket.on('close', () => {
  socket.destroy();
});