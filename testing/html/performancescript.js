var ip = window.location.hostname;

var performanceSocket = new WebSocket(ip + ":5558");

performanceSocket.onmessage = function(event){

var str = event.data;

var performanceArray = str.split(' '),
    ram = Math.round(performanceArray[0]), cpu = Math.round(performanceArray[1]), cpuTemp = Math.round(performanceArray[2]);
	
if (ram < 1024) {
	document.getElementById("ram").innerHTML = "" + ram + " MB";
}
else {
	document.getElementById("ram").innerHTML = "" + (ram/1024).toFixed(2) + " GB";
}

document.getElementById("ramPercentage").className = "c100 big orange p" + Math.round((ram/3963)*100);

document.getElementById("cpu").innerHTML = "" + cpu + "%";
document.getElementById("cpuPercentage").className = "c100 big orange p" + cpu;

document.getElementById("cpuTemp").innerHTML = "" + cpuTemp + "%";
document.getElementById("cpuTempPercentage").className = "c100 big orange p" + cpuTemp;	
}
