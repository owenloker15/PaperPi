async function loadPluginCards() {
  const container = document.getElementById("plugin-grid");
  if (!container) return;

  container.innerHTML = "";

  try {
    const res = await fetch("/playlist/settings");
    const data = await res.json();

    (data.settings || []).forEach((plugin) => {
      const card = document.createElement("div");
      card.className = "card stack";

      const refresh = plugin.refreshSettings || {};
      const schedule = plugin.scheduleSettings || {};

      card.innerHTML = `
        <h3>${plugin.pluginName}</h3>

        ${
          Object.keys(refresh).length
            ? `<div><strong>Refresh:</strong>
               ${refresh.days ?? 0}d
               ${refresh.hours ?? 0}h
               ${refresh.minutes ?? 0}m
               ${refresh.seconds ?? 0}s
               </div>`
            : ""
        }

        ${
          schedule.dailyTime
            ? `<div><strong>Daily Time:</strong> ${schedule.dailyTime}</div>`
            : ""
        }
      `;

      container.appendChild(card);
    });
  } catch (err) {
    console.error("Failed to load plugin cards", err);
  }
}

async function savePluginSettings() {
  const id = document.getElementById("refresh-settings").value;

  const payload = {
    days: Number(document.getElementById("refresh-days").value) || 0,
    hours: Number(document.getElementById("refresh-hours").value) || 0,
    minutes: Number(document.getElementById("refresh-minutes").value) || 0,
    seconds: Number(document.getElementById("refresh-seconds").value) || 0,
  };

  try {
    const res = await fetch(`/playlist/${id}/refresh`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const result = await res.json();
    alert(JSON.stringify(result));
    loadPluginCards();
  } catch (err) {
    console.error("Failed to save refresh settings", err);
  }
}

async function addSchedule() {
  const id = document.getElementById("schedule-time-dropdown").value;
  const time = document.getElementById("schedule-time").value;

  try {
    const res = await fetch(`/playlist/${id}/schedule`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ dailyTime: time }),
    });

    const result = await res.json();
    alert(JSON.stringify(result));
    loadPluginCards();
  } catch (err) {
    console.error("Failed to save schedule", err);
  }
}

async function loadRefreshSettings(pluginId) {
  try {
    const res = await fetch(`/playlist/${pluginId}/refresh`);
    const data = await res.json();

    const fields = ["days", "hours", "minutes", "seconds"];
    fields.forEach((f) => {
      document.getElementById(`refresh-${f}`).value = data.success
        ? data.refresh_settings[f]
        : 0;
    });
  } catch (err) {
    console.error(err);
  }
}

async function loadScheduleSettings(pluginId) {
  try {
    const res = await fetch(`/playlist/${pluginId}/schedule`);
    const data = await res.json();

    document.getElementById("schedule-time").value = data.success
      ? data.plugin_schedule.dailyTime
      : "00:00";
  } catch (err) {
    console.error(err);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const refreshDropdown = document.getElementById("refresh-settings");
  const scheduleDropdown = document.getElementById("schedule-time-dropdown");

  if (refreshDropdown) {
    refreshDropdown.addEventListener("change", (e) =>
      loadRefreshSettings(e.target.value),
    );
    loadRefreshSettings(refreshDropdown.value);
  }

  if (scheduleDropdown) {
    scheduleDropdown.addEventListener("change", (e) =>
      loadScheduleSettings(e.target.value),
    );
    loadScheduleSettings(scheduleDropdown.value);
  }

  loadPluginCards();
});
