//This function is not complete, it has been made for the demo day.
async function goToWell() {
  plate = document.getElementById("wellPlate_select").value;
  plateType = document.getElementById("wellPlate|1").className;
  destination = document.getElementById("selected_well_input").value;
  //Because this is the demo function, and we only use "WellPlate|1" we get the plate from the dropdown and not from the destination
  destination = destination.slice(0, 2);

  console.log(
    `moving to ${destination} on plate ${plate} of type ${plateType}`
  );
  await fetch(`/api/movetowell?plateType=${plateType}&plateNumber=${plate}&coordinate=${destination}`);
  getpos();
}

let lastClicked = 0;
let title = document.title;
let counter = 0;
async function wellClicked(well) {

  // This is in the microscope control website.
  if (title == "Microscope Control") {
    well.className = "selected_well";
    if (lastClicked != 0) {
      lastClicked.className = "well";
    }

    console.log(well.id);
    lastClicked = well;
    document.getElementById("selected_well_input").value = well.id;


    //This is if we are in the routine builder.
  } else if (title == "Routine builder") {
    wellPlateNr = well.id.split("|")[1];
    counter = counter + 1;
    console.log(counter);
    if (counter == 1) {
      well.className = "selected_well";
      lastClicked = well;
    }
    if (counter == 2) {
      // Select everything between the two wells.
      // This only works in one direction, will be fixed.

      //Sometimes this just does not work? especially for the 384 well plates.
      console.log("last clicked: " + lastClicked.id);
      let coord1 = lastClicked.id.split("|")[0];
      let coord2 = well.id.split("|")[0];

      let wellArray1 = [
        coord1[0],
        coord1.replace(/\D/g, ""),
      ];
      
      let wellArray2 = [
        coord2[0],
        coord2.replace(/\D/g, ""),
      ];

      console.log("you pressed: " + wellArray1 + " and " + wellArray2);      
      console.log("it will try to fill from: " + wellArray1[1] + " to " + wellArray2[1]+ " and from " + wellArray1[0] + " to " + wellArray2[0] + " these letters corespond to :" + wellArray1[0].charCodeAt(0) + " and " + wellArray2[0].charCodeAt(0));
      for (let i = wellArray1[1], j = wellArray2[1]; i <= j; i++) {
        console.log(i);
        for (let k = wellArray1[0].charCodeAt(0), l = wellArray2[0].charCodeAt(0); k <= l; k++) {

          document.getElementById(String.fromCharCode(k) + i + "|" + wellPlateNr).className = "selected_well";
          console.log("filling: " + String.fromCharCode(k) + i + "|" + wellPlateNr);

        }
      }
    
    }
    if (counter == 3) {
      counter = 0;
      removeSelected();      
    }
  
  }
}

async function removeSelected() { 
  counter = 0;
  console.log("removing selected");
  collection = document.querySelectorAll("td.selected_well");
  for (well in collection) {
    collection[well].className = "well";
  }
}

// Call this function with the size and the location you want to place the well plate.
//  <table id="wellPlate|x" class="tableSize"></table>;
//where x is the wellPlateNr

async function chooseWellPlate(size, wellPlateNr) {
  counter = 0;
  if (size == 48) {
   
  }
  if (size == 96) {
    i_max = 8;
    j_max = 12 + 1;
  } else if (size == 384) {
    i_max = 16;
    j_max = 24 + 1;
  } else if (size == 48) {
     i_max = 6;
     j_max = 8 + 1;
  } else if (size == 1536) {
    console.log("not supported yet!");
  } else {
    console.log("Well plate size not supported");
    return null;
  }
  //replace the old one if there already exsists one.
  if (document.getElementById("wellPlate" + "|" + wellPlateNr) != null) {
    document.getElementById("wellPlate" + "|" + wellPlateNr).remove();
    var wellplateDiv = document.getElementById("div_wellplate");
    var wellPlateTable = document.createElement("table");
    if (size == 96) {
      wellPlateTable.className = "WellPlateType96";
    } else if (size == 384) {
      wellPlateTable.className = "WellPlateType384";
    } else if (size == 48) {
      wellPlateTable.className = "WellPlateType48";
    }
    wellPlateTable.id = "wellPlate" + "|" + wellPlateNr;
    wellplateDiv.appendChild(wellPlateTable);
  }
  //Table header row
  let headerRow = document.createElement("tr");
  headerRow.id = "headerRow" + "|" + wellPlateNr;
  wellPlateTable.appendChild(headerRow);
  for (let i = 1; i < j_max; i++) {
    if (i == 1) {
      let emptyCell = document.createElement("td");
      headerRow.appendChild(emptyCell);
    }
    let headerCell = document.createElement("th");
    headerCell.id = "headerCell" + "|" + wellPlateNr;
    headerCell.innerHTML = i;
    headerRow.appendChild(headerCell);
  }
  //table content
  for (let i = 0; i < i_max; i++) {
    let row = document.createElement("tr");
    row.id = String.fromCharCode(65 + i) + "|" + wellPlateNr;
    let headerColumnCell = document.createElement("th");
    headerColumnCell.id = "headerColumnCell" + i + "|" + wellPlateNr;
    headerColumnCell.innerHTML = String.fromCharCode(65 + i);

    document.getElementById("wellPlate" + "|" + wellPlateNr).appendChild(row);
    document
      .getElementById(String.fromCharCode(65 + i) + "|" + wellPlateNr)
      .appendChild(headerColumnCell);

    for (let j = 1; j < j_max; j++) {
      let well = document.createElement("td");
      well.innerHTML = String.fromCharCode(65 + i) + j;
      well.id = well.innerHTML + "|" + wellPlateNr;
      well.className = "well";
      well.data = well.style.backgroundColor;
      well.onclick = function () {
        wellClicked(well);
      };

      document.getElementById(row.id).appendChild(well);
    }
  }
}
