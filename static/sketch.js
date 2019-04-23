var space;
var marginY;
var buttonPower, buttonReboot, buttonStart, buttonStop, buttonTest, buttonTestSerial;
var started = false;
var rt;

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
  buttonTest = createButton('PARALLEL TEST');
  buttonTest.position(space, 130);
  buttonTest.mouseClicked(testParallel);
  buttonTestSerial = createButton('SERIAL TEST');
  buttonTestSerial.position(space+122, 130);
  buttonTestSerial.mouseClicked(testSerial);

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
	
	var dataParsed;
	var textMargY = 200;
	if(initData != undefined){
	  dataParsed = JSON.parse(initData);
	  //text(initData,space, height-30); 
	  text("N_STATES: "+dataParsed.N_STATES.toString(),space, height-textMargY); 
	  text("ACTIONS: "+dataParsed.ACTIONS.toString(),space, height-textMargY+15);
	  text("EPSILON: "+dataParsed.EPSILON.toString(),space, height-textMargY+30);
	  text("ALPHA: "+dataParsed.ALPHA.toString(),space, height-textMargY+45);
	  text("GAMMA: "+dataParsed.GAMMA.toString(),space, height-textMargY+60);
	  text("MAX_EPISODES: "+dataParsed.MAX_EPISODES.toString(),space, height-textMargY+75);
	  text("REFRESH_TIME_MIN: "+dataParsed.REFRESH_TIME_MIN.toString(),space, height-textMargY+90);
	  text("REFRESH_TIME_MAX: "+dataParsed.REFRESH_TIME_MAX.toString(),space, height-textMargY+105);
	}
	var rtDataParsed;
	if(rtData != undefined && started){
	  rtDataParsed = JSON.parse(rtData);
	  rt = rtDataParsed.RT;
	  console.log(rt);
	}

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
	  var numb = rt[i];
	  numb = Math.floor(numb*100)/100;
	  text("M"+i.toString(),space+i*space-10, marginY+30); 
	  text("A: "+ d[i].toString(),space+i*space-10, marginY+50); 
	  text("RT: " +  numb.toString(), space+i*space-10, marginY+70);
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

function testParallel(){
	var res = confirm("This will run a TEST of ALL Motors simultaneously");
	if (res){
	  socket.emit('test', {'data': "p"});
	}
}

function testSerial(){
	var res = confirm("This will run a TEST of ALL Motors ONE by ONE");
	if (res){
	  socket.emit('test', {'data': "s"});
	}
}
