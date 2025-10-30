let mode = 'manual';
let currentDate = 1;
const totalDates = 20;
let startTime;

let participantId = prompt("Enter your Participant ID (e.g., P01):");
if (!participantId) {
  participantId = "P00"; //default
}


function switchMode(selectedMode) {
  mode = selectedMode;
  currentDate = 1;
  renderInput();
}


function renderInput() {
  const container = document.getElementById('experiment');
  const progress = document.getElementById('progress');
  progress.innerText = `Entry ${currentDate} of ${totalDates}`;

  let html = '';
  if (mode === 'manual') {
    html = `
      <label>Enter date (YYYY-MM-DD):</label>
      <input id="manualInput" type="text">
      <button onclick="submitManual()">Submit</button>`;
  } else if (mode === 'calendar') {
    html = `
      <label>Select a date:</label>
      <input type="text" id="calendarInput" placeholder="Select date">
      <button onclick="submitCalendar()">Submit</button>`;
  } else {
    html = `
      <label>Enter or select a date:</label>
      <input type="text" id="hybridInput" placeholder="YYYY-MM-DD">
      <input type="text" id="calendarInput" placeholder="Select date">
      <button onclick="submitHybrid()">Submit</button>`;
  }

  container.innerHTML = html;

  const calendarInput = document.getElementById('calendarInput');
  if (calendarInput) {
    jSuites.calendar(calendarInput, {
      type: 'year-month-day',
      format: 'YYYY-MM-DD',
    });
  }

  startTime = performance.now();
}

function logResult(method, value) {
  const timeTaken = performance.now() - startTime;

  fetch("http://localhost:8000/api/log", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ participant_id: participantId, method, value, timeTaken })
  });

  currentDate++;
  if (currentDate > totalDates) {
  } else {
    renderInput();
  }
}

function submitManual() {
  const input = document.getElementById('manualInput').value;
  logResult('manual', input);
}

function submitCalendar() {
  const input = document.getElementById('calendarInput').value;
  logResult('calendar', input);
}

function submitHybrid() {
  const textVal = document.getElementById('hybridInput').value;
  const calVal = document.getElementById('calendarInput').value;
  const finalVal = calVal || textVal;
  logResult('hybrid', finalVal);
}

renderInput();
