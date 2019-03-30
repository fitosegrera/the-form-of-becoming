var space;
var marginY;
var buttonPower, buttonReboot, buttonStart, buttonStop;
var started = false;

function setup() { 
  createCanvas(windowWidth, windowHeight);
  space = windowWidth/17;
  marginY = windowHeight/2;
  buttonStart = createButton('START');
  buttonStart.position(space, 40);
  buttonStart.mouseClicked(start);
  buttonStop = createButton('STOP');
  buttonStop.position(space+60, 40);
  buttonStop.mouseClicked(stop);
  buttonPower = createButton('SHUTDOWN PC');
  buttonPower.position(space, 70);
  buttonPower.mouseClicked(shutDown);
  buttonReboot = createButton('REBOOT PC');
  buttonReboot.position(space, 100);
  buttonReboot.mouseClicked(rebootPc);
} 

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
  space = windowWidth/17;
  marginY = windowHeight/2;
}

function draw() { 
	background(0);
	fill(255);
	stroke(255);
	strokeWeight(5);
	line(space, marginY, width-space, marginY);
	strokeWeight(0.5);
	text(status, space + 20, 25);
	if(status == "connected"){
	  fill(0, 255, 0);
	}else{
		fill(255, 0, 0);
	}
	if(status == "disconnected" || !started){
	  for(var i=0; i<d.length; i++){
	    d[i] = 0;
	  }
	}
	ellipse(space + 5, 20, 10, 10);
	fill(255);
	text(initData,space, height-30); 
	for (var i=0; i<d.length; i++){
	  ellipse(space+i*space,marginY-map(d[i],0,180,0,100),5,5);
	  if(i>0){
	    line(space+(i-1)*space, marginY-map(d[i-1],0,180,0,100), space+i*space, marginY-map(d[i],0,180,0,100));
	  }
	  if(d[i] == 180){
	    rectMode(CENTER);
	    rect(space+i*space, marginY-map(d[i],0,180,0,100) - 20, space/2, 5);
	    rectMode(CORNER);
	  }
	  text(d[i],space+i*space, marginY+30); 
	}
      
}

function start(){
	socket.emit('start', {'data': true});
	started = true;
}

function shutDown(){
	var res = confirm("Are you sure you want to turn OFF the PC?");
	if (res){
		socket.emit('power', {'data': "OFF"});
	}
}

function rebootPc(){
	var reb = confirm("Are you sure you want to REBOOT the PC?");
	if (reb){
		socket.emit('reboot', {'data': "REBOOT"});
	}
}

function stop(){
	socket.emit('stop', {'data': true});
	started = false;
	for(var i=0; i<d.length; i++){
	    d[i] = 0;
	}
}
