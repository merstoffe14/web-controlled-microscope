async function relStep(direction, sign) {
  stepsize = document.getElementById("stepSize_range_label").value;

  if (sign == "m") {
    stepsize = -stepsize;
  }
  if (sign == "p") {
    stepsize = stepsize;
  }
  if (direction == "x") {
    x = stepsize;
    y = 0;
    z = 0;
  }
  if (direction == "y") {
    x = 0;
    y = stepsize;
    z = 0;
  }
  if (direction == "z") {
    x = 0;
    y = 0;
    z = stepsize;
  }
  await fetch(`/api/goto?x=${x}&y=${y}&z=${z}&sys=${1}`);

  getpos();
}

async function submitStepSizeChange(value) {
  console.log("submitted: " + value);
  if (value > 5) {
    val = 5;
  }
  if (value < 0.01) {
    val = 0.01;
  } else {
    val = value;
  }

  document.getElementById("stepSize_range").value = val;
  document.getElementById("stepSize_range_label").value = val;
}

//loop while key down
document.onkeydown = function (e) {
  btn_left = document.getElementById("btn_left");
  btn_right = document.getElementById("btn_right");
  btn_up = document.getElementById("btn_up");
  btn_down = document.getElementById("btn_down");
  z_plus = document.getElementById("zplus_rel_button");
  z_minus = document.getElementById("zmin_rel_button");

  if (e.key == "ArrowUp") {
    e.view.event.preventDefault();
    btn_up.click();
    console.log("up");
  }
  if (e.key == "ArrowDown") {
    e.view.event.preventDefault();
    btn_down.click();
    console.log("down");
  }
  if (e.key == "ArrowLeft") {
    e.view.event.preventDefault();

    btn_left.click();
    console.log("left");
  }
  if (e.key == "ArrowRight") {
    e.view.event.preventDefault();

    btn_right.click();
    console.log("right");
  }
  if (e.key == "p") {
    z_plus.click();
    console.log("z+");
  }
  if (e.key == "m") {
    z_minus.click();
    console.log("z-");
  }
};
