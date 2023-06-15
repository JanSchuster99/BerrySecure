const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const generateBtn = document.getElementById("generate-btn");
const quantityInput = document.getElementById("quantity-input");
const numBitsInput = document.getElementById("numBits-input");
const resultTable = document.getElementById("result-table");
const toggleBtn = document.getElementById("toggleBtn");
let isRunning = false;
// Set initial state of buttons


// Start button
startBtn.addEventListener("click", async () => {
    try{
      // Initialize system
      const response = await fetch("https://172.16.78.55:8080/trng/randomNum/init");
      // Show status codes as pop up windows
      if(!response.ok){
        console.log("Error:" + response.status);
        if(response.status == 445){
          alert("Error: "+ response.status +"\nMicrophone not connected. Please connect the microphone and try again.");
        }
        else if(response.status == 555){
          alert("Error: "+ response.status +"\nUnable to initialize the random number generator within a timeout of 60 seconds.");
        }
        else if(response.status == 543){
          alert("Error: "+ response.status +"\nStartup test failed. Try again.");
        }
        else if(response.status == 409){
          alert("Error: "+ response.status +"\nSystem is already running.");
        }
        return;
      }
      console.log("Started");
      isRunning = true;
    }
    catch(error){
      console.error(error);
    }
  });

  stopBtn.addEventListener("click", async () => {    
    try{
      const response = await fetch("https://172.16.78.55:8080/trng/randomNum/shutdown");
      if(!response.ok){
        console.log("Error:" + response.status);
        if(response.status == 409){
          alert("Error: "+ response.status +"\nSystem already shutdown.");
        }
        return;
      }
      console.log("Stopped");
      isRunning = false;
    }
    catch(error) {
        console.error(error);
    }
  });

// Generate button
generateBtn.addEventListener("click", async () => {
  const quantity = quantityInput.value;
  const numBits = numBitsInput.value;
  const url = `https://172.16.78.55:8080/trng/randomNum/getRandom?quantity=${quantity}&numBits=${numBits}`;
  resetTable();
  showSpinner();

  try{
    // Generate numbers with input parameters
    const response = await fetch(url);
    // Show status codes as pop up windows
    if(!response.ok){
      console.log("Error:" + response.status);
      if(response.status == 432){
        alert("Error: "+ response.status +"\nSystem not ready. Please try again.");
        hideSpinner();
      }
      else if(response.status == 400){
        alert("Error: "+ response.status +"\nOnly numeric input greater than 0 and no more than 67108864 is allowed. Please enter valid input only.");
        hideSpinner();
      }
      else if(response.status == 445){
        alert("Error: "+ response.status +"\nMicrophone not connected. Please connect the microphone and try again.");
        hideSpinner();
      }
      else if(response.status == 543){
        alert("Error: "+ response.status +"\nOnline Test failed. Please try again.");
        hideSpinner();
      }
      else if(response.status == 500){
        alert("Error: "+ response.status +"\nInternal Server Error. Please restart the system.");
        hideSpinner();
      }
      return;
    }
    // Output data in table
    const data = await response.json();
    console.log(data.randomBits);
    exportToFile(data.randomBits);
    const tableRows = data.randomBits.map((num, index) => {
      const tableData1 = document.createElement("td");
      const tableData2 = document.createElement("td");
      const tableData3 = document.createElement("td");
      tableData1.textContent = index + 1;

      // Copy button
      const button = document.createElement("button");
      button.textContent = "Copy";
      button.addEventListener("click", function () {
        console.log("Button clicked");
        copyRow(this.parentNode.parentNode);
      });
      tableData2.appendChild(button);
      tableData3.textContent = num;
      const tableRow = document.createElement("tr");
      tableRow.appendChild(tableData1);
      tableRow.appendChild(tableData2);
      tableRow.appendChild(tableData3);
      return tableRow;
      });
      resultTable.innerHTML =
        "<tr><th>Nr.</th><th>Actions</th><th>Random Hex Values</th></tr>";
      tableRows.forEach((row) => resultTable.appendChild(row));
      hideSpinner();
  }
  catch(error){
    console.error(error);
  }

});

function copyRow(row) {
  const numberValue = row.querySelector("td:nth-child(3)").textContent;
  navigator.clipboard.writeText(numberValue);
}

function exportToFile(hexArray) {
  const fileContents = hexArray.join('\n');

  const blob = new Blob([fileContents], { type: 'text/plain' });

  const button = document.getElementById('export-btn');
  button.disabled = false;
  button.textContent = 'Export Random Hex Values';
  button.onclick = () => {
    const link = document.createElement('a');
    link.download = "random_hex_values_" + getCurrentDate() + ".txt";
    link.href = window.URL.createObjectURL(blob);
    link.onclick = () => {
      setTimeout(() => {
        window.URL.revokeObjectURL(blob);
        link.remove();
      }, 0);
    };
    document.body.appendChild(link);
    link.click();
  };
}

function getCurrentDate() {
  const now = new Date();
  const year = now.getFullYear();
  const month = now.getMonth() + 1;
  const day = now.getDate();
  const hours = now.getHours();
  const minutes = now.getMinutes();
  const seconds = now.getSeconds();

  const formattedDateTime = `${year}_${month < 10 ? "0" : ""}${month}_${day < 10 ? "0" : ""
    }${day}_${hours < 10 ? "0" : ""}${hours}_${minutes < 10 ? "0" : ""
    }${minutes}_${seconds < 10 ? "0" : ""}${seconds}`;

  return formattedDateTime;
}

function showSpinner() {
  console.log("showSpinner");
  const spinner = document.getElementById("loading-spinner");
  spinner.style.display = "block";
}

function hideSpinner() {
  const spinner = document.getElementById("loading-spinner");
  spinner.style.display = "none";
}

function resetTable() {
  var table = document.getElementById("result-table");
  var rowCount = table.rows.length;
  for (var i = rowCount - 1; i > 0; i--) {
    table.deleteRow(i);
  }
}