let mode = 'manual';
let currentDate = 1;
const totalDates = 20;
let startTime;

function switchMode(selectedMode) {
  mode = selectedMode;
  currentDate = 1;
  renderInput();
}

function showMessage(text) {
  document.getElementById('message').innerText = text;
}

function renderInput() {
  const container = document.getElementById('experiment');
  const progress = document.getElementById('progress');
  progress.innerText = `Date ${currentDate} of ${totalDates}`;
  
  let html = '';
  if (mode === 'manual') {
    html = `
      <label>Enter date (YYYY-MM-DD):</label>
      <input id="manualInput" type="text">
      <button onclick="submitManual()">Submit</button>`;
  } else if (mode === 'calendar') {
    html = `
      <label>Select a date:</label>
      <input type="date" id="calendarInput" max="${new Date().toISOString().split('T')[0]}">
      <button onclick="submitCalendar()">Submit</button>`;
  } else {
    html = `
      <label>Enter or select a date:</label>
      <input type="text" id="hybridInput" placeholder="YYYY-MM-DD">
      <input type="date" id="calendarInput" max="${new Date().toISOString().split('T')[0]}">
      <button onclick="submitHybrid()">Submit</button>`;
  }

  container.innerHTML = html;
  startTime = performance.now();
}

function logResult(method, value, error=false) {
  const timeTaken = performance.now() - startTime;
  showMessage(`Method: ${method}, Value: ${value}, Time: ${Math.round(timeTaken)} ms`);

  fetch("http://localhost:5000/api/log", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ method, value, timeTaken, error })
  });

  currentDate++;
  if (currentDate > totalDates) {
    showMessage("Experiment complete");
  } else {
    renderInput();
  }
}

function submitManual() {
  const input = document.getElementById('manualInput').value;
  const error = !/^\d{4}-\d{2}-\d{2}$/.test(input);
  logResult('manual', input, error);
}

function submitCalendar() {
  const input = document.getElementById('calendarInput').value;
  const error = !input;
  logResult('calendar', input, error);
}

function submitHybrid() {
  const textVal = document.getElementById('hybridInput').value;
  const calVal = document.getElementById('calendarInput').value;
  const finalVal = calVal || textVal;
  const error = !/^\d{4}-\d{2}-\d{2}$/.test(finalVal);
  logResult('hybrid', finalVal, error);
}

renderInput();
