// Drawing on the webplatform, by Edgar Cardenas

function convertAbsoluteToActual(x, y, z, sys) {
  actual_limits = machineLimits;
  //THESE VALUES SHOULD CHANGE IF THE CANVAS IS CHANGED.

  let canvas = document.getElementById("position_canvas");
  s = canvas.width / 320;

  absolute_limits_lower = [30 * s, 30 * s, 3];
  absolute_limits_upper = [297 * s, 306 * s, 194];

  if (sys == 0) {
    actual_x =
      ((x - absolute_limits_lower[0]) /
        (absolute_limits_upper[0] - absolute_limits_lower[0])) *
      actual_limits[0];
    actual_y =
      ((y - absolute_limits_lower[1]) /
        (absolute_limits_upper[1] - absolute_limits_lower[1])) *
      actual_limits[1];
    actual_z =
      ((absolute_limits_lower[2] - z) /
        (absolute_limits_upper[2] - absolute_limits_lower[2])) *
        actual_limits[2] +
      actual_limits[2];

    return [actual_x, actual_y, actual_z];
  }

  //Inverse
  if (sys == 1) {
    pixel_x =
      (x / actual_limits[0]) *
        (absolute_limits_upper[0] - absolute_limits_lower[0]) +
      absolute_limits_lower[0];
    pixel_y =
      (y / actual_limits[1]) *
        (absolute_limits_upper[1] - absolute_limits_lower[1]) +
      absolute_limits_lower[1];
    pixel_z =
      (z / actual_limits[2]) *
        (absolute_limits_lower[2] - absolute_limits_upper[2]) +
      absolute_limits_upper[2];

    return [pixel_x, pixel_y, pixel_z];
  }
}

function setXYposition(event) {
  let canvas = document.getElementById("position_canvas");
  let rect = canvas.getBoundingClientRect();
  let x = event.clientX - rect.left;
  let y = event.clientY - rect.top;

  scale = canvas.width / 320;

  let limits = [30 * scale, 30 * scale, 297 * scale, 306 * scale];

  // These should change if the canvas is changed
  if (x < limits[0] || y < limits[1]) {
    return;
  }
  if (x > limits[2] || y > limits[3]) {
    return;
  }

  draw_top_layout();
  draw_position_xy(x, y);

  console.log("Coordinate x: " + x, "Coordinate y: " + y);
}

function draw_top_layout() {
  let canvas = document.getElementById("position_canvas");
  scale = canvas.width / 320;
  let ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  ctx.beginPath();
  ctx.lineWidth = "3";
  ctx.strokeStyle = "#DDD";
  ctx.rect(10, 10, canvas.width - 20, canvas.height - 20);
  ctx.fillStyle = "#333";
  ctx.fill();
  ctx.stroke();

  let h = 85.4 * scale;
  let w = 128.3 * scale;
  let py = 9.6 * scale;
  let px = 9.7 * scale;

  for (let ix = 0; ix < 2; ix++) {
    for (let iy = 0; iy < 3; iy++) {
      ctx.beginPath();
      ctx.lineWidth = "1";
      ctx.strokeStyle = "blue";
      ctx.rect(30 + (w + px) * ix, 30 + (h + py) * iy, w, h);
      ctx.fillStyle = "#555";
      ctx.fill();
      ctx.stroke();
    }
  }
}

function draw_position_xy(x, y) {
  let canvas = document.getElementById("position_canvas");
  let ctx = canvas.getContext("2d");

  ctx.beginPath();
  ctx.arc(x, y, 3, 0, 2 * Math.PI, false);
  ctx.fillStyle = "red";
  ctx.fill();

  actual = convertAbsoluteToActual(x, y, 0, 0);

  document.getElementById("x_input").value = actual[0];
  document.getElementById("y_input").value = actual[1];
}

function setZposition(event) {
  let canvas = document.getElementById("position_canvas");
  let rect = canvas.getBoundingClientRect();
  let z = event.clientY - rect.top;

  draw_side_layout(z);

  console.log("Coordinate Z: " + z);
}

function draw_side_layout(z) {
  if (z > 195) {
    z = 195;
  }
  if (z < 3) {
    z = 3;
  }

  actual = convertAbsoluteToActual(0, 0, z, 0);
  document.getElementById("z_input").value = actual[2];

  let canvas = document.getElementById("zposition_canvas");
  let ctx = canvas.getContext("2d");

  let pad = 10;
  let scope_length = 180;
  z = z + scope_length + pad;

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  ctx.beginPath();
  ctx.lineWidth = "3";
  ctx.strokeStyle = "#FFF";
  ctx.rect(pad, pad, canvas.width - 2 * pad, canvas.height - 2 * pad);
  ctx.fillStyle = "#333";
  ctx.fill();
  ctx.stroke();

  ctx.beginPath();
  ctx.lineWidth = "1";
  ctx.strokeStyle = "#33B";
  ctx.rect(20, z - scope_length, 40, scope_length);
  ctx.fillStyle = "#228";
  ctx.fill();
  ctx.stroke();

  ctx.beginPath();
  ctx.lineWidth = "3";
  ctx.strokeStyle = "#DDD";
  ctx.rect(canvas.width - 30, 10, 10, canvas.height - 20);
  ctx.fillStyle = "#222";
  //ctx.fill();
  ctx.stroke();

  ctx.beginPath();
  ctx.lineWidth = "1";
  ctx.strokeStyle = "#E33";
  ctx.rect(10, z - 60, 60, 60);
  ctx.fillStyle = "#811";
  ctx.fill();
  ctx.stroke();

  ctx.beginPath();
  ctx.lineWidth = "1";
  ctx.strokeStyle = "#33E";
  ctx.rect(30, z - 40, 90, 20);
  ctx.fillStyle = "#118";
  ctx.fill();
  ctx.stroke();

  ctx.beginPath();
  ctx.arc(40, z - scope_length, 3, 0, 2 * Math.PI, false);
  ctx.fillStyle = "red";
  ctx.fill();
}
