selectedList = [];


async function confirmWellSelection() { 
    selectedList = [];
    collection = document.querySelectorAll("td.selected_well");
    console.log(collection);
    count = 0;
    z_offset = 0;
    for (well in collection) {
        //This loops too much?
        selectedList[count] = [collection[well].id, z_offset];
        count++;
    }
    console.log(selectedList);
}

async function update_zscan_preview() { 

    let z0 = document.getElementById("zscan_min_range").value;
    let z1 = document.getElementById("zscan_max_range").value;
    let zstep = document.getElementById("zscan_step_range").value

    z0 = Number(z0)
    z1 = Number(z1)
    zstep = Number(zstep)

    if (z0 > z1) {z0 = (z1-1);}
    if (z1 < z0) {z1 = z0+1;}    

    document.getElementById("zscan_min_range").value = z0
    document.getElementById("zscan_max_range").value = z1
    document.getElementById("zscan_step_range").value = zstep

    z0 = (z0 + 10)*5.
    z1 = (z1 + 10)*5.
    zstep = (zstep)*5.

    //if (z0 > 190) { z0 = 190; }
    //if (z0 < 3) {  z0 = 3; }

    //if (z1 > 195) { z1 = 195; }
    //if (z1 < 5) {  z1 = 5; }

    //if (zstep < 0.1){zstep=0.1;}

    let canvas = document.getElementById("zscan_canvas");
    let ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.beginPath();
    
    for (var i = z0; i < z1; i+=zstep) {
        ctx.arc(40, i, 3, 0, 2 * Math.PI, false);
        ctx.fillStyle = "green";
    }

    ctx.fill();


}

async function do_z_scan() {

    let z0 = document.getElementById("zscan_min_range").value;
    let z1 = document.getElementById("zscan_max_range").value;
    let zstep = document.getElementById("zscan_step_range").value

    await fetch(`/api/dozscan?start=${z0}&end=${z1}&step=${zstep}`);
  }


