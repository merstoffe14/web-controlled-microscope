main()
    .then(_ => {

    })
    .catch(err => {
        console.error(err);
    });

async function main() {
    locationBook = await fetchData();
    refreshSelect(locationBook);
}

async function refreshSelect(locationBook) {

    x = document.getElementById("location_select")
    var i, L = x.options.length - 1;
    for (i = L; i >= 0; i--) {
        x.remove(i);
    }

    for (let i in locationBook) {
        var option = document.createElement("option");
        option.text = i;
        x.add(option);
        console.log(i);
    }

}


async function fetchData() {
    console.log("Fetching data");
    let dataResponse = await fetch("/api/getdata");
    let data = await dataResponse.json();
    locationBook = data;
    console.log(locationBook);
    return locationBook;
}


function selected() {
    var selected = document.getElementById("location_select").value
    if (!(selected in locationBook)) {
        console.log("Selection does not exist")
        return
    }

    document.getElementById("x_form").value = locationBook[selected][0]
    document.getElementById("y_form").value = locationBook[selected][1]
    document.getElementById("z_form").value = locationBook[selected][2]

    // Needs conversion from absolute to actual coords

    pixel_locations = convertAbsoluteToActual(locationBook[selected][0], locationBook[selected][1], locationBook[selected][2],1)

    draw_top_layout();
    draw_side_layout(pixel_locations[2]);
    draw_position_xy(pixel_locations[0], pixel_locations[1]);

}

async function lock() {
    text = document.getElementById("lock_button").innerHTML;

    if (text == "Lock") {
        document.getElementById("lock_button").innerHTML = "Unlock";
        document.getElementById("x_form").disabled = true;
        document.getElementById("y_form").disabled = true;
        document.getElementById("z_form").disabled = true;
    }
    if (text == "Unlock") {
        document.getElementById("lock_button").innerHTML = "Lock";
        document.getElementById("x_form").disabled = false;
        document.getElementById("y_form").disabled = false;
        document.getElementById("z_form").disabled = false;
    }

}

async function save() {
    x = document.getElementById("x_form").value;
    y = document.getElementById("y_form").value;
    z = document.getElementById("z_form").value;
    name = document.getElementById("location_select").value;

    console.log(x, y, z, name);
    await fetch(`/api/updatelocationlist?x=${x}&y=${y}&z=${z}&name=${name}`);
    main();

}

async function addNewFromCurrent() { 


}

async function goToLm() {

    x = document.getElementById("x_form").value;
    y = document.getElementById("y_form").value;
    z = document.getElementById("z_form").value;
    console.log(x, y, z);
    await fetch(`/api/goto?x=${x}&y=${y}&z=${z}&sys=${0}`);

}