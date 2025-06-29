async function setupCameraSettings() {



  //Get the saved camera settings [NOT YET IMPLEMENTED]
  // while not implemented: get the standard values
  exposure = document.getElementById('exposureTime_range').value
  gain = document.getElementById('gain_range').value
  contrast = document.getElementById('contrast_range').value

  //Set the camera settings to the values on the webpage
  // await fetch(`/api/setcamerasetting?setting=Contrast&value=${contrast}`)}`);
  await fetch(`/api/setcamerasetting?setting=Gain&value=${gain}`);
  await fetch(`/api/setcamerasetting?setting=ExposureTime&value=${exposure}`);
}


async function submitExposureTimeChange(value) {
  console.log("submitted: " + value + " exposure time");
  if (value > 1410065) {
    val = 1410065;
  }
  if (value < 5) {
    val = 5;
  } else {
    val = value;
  }

  document.getElementById("exposureTime_range_label").value = val;
  document.getElementById("exposureTime_range").value = val;
  await fetch(`/api/setcamerasetting?setting=ExposureTime&value=${val}`);


}


async function submitGainChange(value) {
  console.log("submitted: " + value + " for gain");
  if (value > 20) {
    val = 20;
  }
  if (value < 0.1) {
    val = 0.1;
  } else {
    val = value;
  }
  document.getElementById("gain_range_label").value = val;
  document.getElementById("gain_range").value = val;
  await fetch(`/api/setcamerasetting?setting=Gain&value=${val}`);
  
}

async function submitContrastChange(value) {
  console.log("submitted: " + value + " for contrast");
  if (value > 20) {
    val = 20;
  }
  if (value < 0.1) {
    val = 0.1;
  } else {
    val = value;
  }
  document.getElementById("contrast_range_label").value = val;
  document.getElementById("contrast_range").value = val;
  // await fetch(`/api/setcamerasetting?setting=Contrast&value=${val}`);
  

}

async function submitBrightnessChange(value) { 
  console.log("submitted: " + value + " for brightness");
  if (value > 12000) {
    val = 12000;
  }
  if (value < 500) {
    val = 500;
  } else {
    val = value;
  }
  lamp_val = val;
  await fetch(`/api/setcamerasetting?setting=Brightness&value=${val}`);

}

//setInterval(submitContrastChange(), 1000)
//setInterval(submitGainChange(), 1000)
//setInterval(submitExposureTimeChange(), 1000)