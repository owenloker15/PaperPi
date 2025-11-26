function addCalendarInput(url = "", color = "#007BFF") {
  const calendarList = document.getElementById("calendars-list");

  const wrapper = document.createElement("div");

  const colorInput = document.createElement("input");
  colorInput.type = "color";
  colorInput.name = "calendarColors[]";
  colorInput.classList.add("color-picker");
  colorInput.value = color;

  const urlInput = document.createElement("input");
  urlInput.type = "text";
  urlInput.name = "calendarURLs[]";
  urlInput.placeholder = "Calendar URL";
  urlInput.classList.add("calendar-url");
  urlInput.required = true;
  urlInput.value = url;

  const removeBtn = document.createElement("button");
  removeBtn.type = "button";
  removeBtn.innerText = "✕";
  removeBtn.classList.add("remove-btn");
  removeBtn.onclick = function () {
    if (calendarList.childElementCount > 1) {
      wrapper.remove();
    }
  };

  wrapper.appendChild(colorInput);
  wrapper.appendChild(urlInput);
  wrapper.appendChild(removeBtn);

  wrapper.classList.add("calendar-entry");

  calendarList.appendChild(wrapper);
}

document.addEventListener("DOMContentLoaded", function () {
  addCalendarInput();
  const layoutRadioButtons = document.querySelectorAll('input[name="layout"]');
  console.log(layoutRadioButtons);
  const timeInterval = document.getElementById("time-interval");
  console.log(timeInterval);

  layoutRadioButtons.forEach((radio) => {
    radio.addEventListener("change", function () {
      if (
        this.checked &&
        (this.value == "timeGridDay" || this.value == "timeGridWeek")
      ) {
        timeInterval.style.display = "block";
        console.log("show time interval");
      } else {
        timeInterval.style.display = "none";
        console.log("hide time interval");
      }
    });
  });
});
