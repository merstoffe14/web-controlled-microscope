// This variable will be set in main()
machineLimits = [0, 0, 0]
lamp_val = 500; //default value, between 500-12000

async function main() {

  //draw plate layout:
  draw_top_layout();
  draw_position_xy(0,0);
  draw_side_layout(0);

  //get current position
  getpos();

  //start the livestream
  await getLiveStream();

  //set-up camera settings
  setupCameraSettings();
  
  //draw the a wellplate
  chooseWellPlate(96, 1);

    //Get the machine limits
    let dataResponse = await fetch("/api/getmachinelimits");
    machineLimits = await dataResponse.json();

}


async function toggleLamp() {
  lamp_button = document.getElementById("lamp_button");
  if (lamp_button.innerHTML == "Lamp: on") {
    lamp_button.innerHTML = "Lamp: off";
    sendCommand("M3 s"+lamp_val);
  } else {
    lamp_button.innerHTML = "Lamp: on";
    sendCommand("M5");
  }
}

async function updateRangeVal(value, id) {
  document.getElementById(id).value = Math.round(value * 100) / 100.0;
}

async function getLiveStream() {
  const socket = new WebSocket(getAbsolutePath(`api/livefeed`));
  socket.binaryType = "arraybuffer";
  socket.addEventListener("message", (e) => {
    base64 = arrayBufferToBase64(e.data);
    img = document.getElementById("liveview");
    img.src = "data:image/png;base64, " + base64;
  });
}

//Base 64 because thats what the image tag wants.
//https://stackoverflow.com/questions/9267899/arraybuffer-to-base64-encoded-string
function arrayBufferToBase64(buffer) {
  var binary = "";
  var bytes = new Uint8Array(buffer);
  var len = bytes.byteLength;
  for (var i = 0; i < len; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return window.btoa(binary);
}

// https://stackoverflow.com/questions/10406930/how-to-construct-a-websocket-uri-relative-to-the-page-uri
function getAbsolutePath(relativeUrl) {
  var loc = window.location,
    new_uri;
  if (loc.protocol === "https:") {
    new_uri = "wss:";
  } else {
    new_uri = "ws:";
  }
  new_uri += "//" + loc.host;
  new_uri += loc.pathname + relativeUrl;
  return new_uri;
}

async function takePicture() {
    await fetch(`/api/takePicture`);
  }

async function sendCommand(command) {
  await fetch(`/api/sendcommand?command=${command}`);
  getpos();
}

async function goTo() {
  x = document.getElementById("x_input").value;
  y = document.getElementById("y_input").value;
  z = document.getElementById("z_input").value;
  console.log(x);
  console.log(x, y, z);
  await fetch(`/api/goto?x=${x}&y=${y}&z=${z}&sys=${0}`);

  getpos();
}

async function calibrate_z() {
  await fetch(`/api/autofocus`);
}

//Gets the position and draws it
async function getpos() {
  let dataResponse = await fetch("/api/getposition");
  let data = await dataResponse.json();

  pixel = convertAbsoluteToActual(data[0], data[1], data[2], 1);

  draw_top_layout();
  console.log("z actual: " + data[2]);
  console.log("z pixel: " + pixel[2]);
  draw_side_layout(pixel[2]);
  draw_position_xy(pixel[0], pixel[1]);
}

function openTab(evt, cityName) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}


main();
