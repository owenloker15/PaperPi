async function updateClicked() {
  const form = document.getElementById("settings-form");
  if (!form) return;

  const formData = new FormData(form);
  const url = form.dataset.submitUrl || window.location.pathname + "/submit";

  try {
    const res = await fetch(url, {
      method: "POST",
      body: formData,
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.error || "Update failed");
    }

    alert("Updated successfully");
  } catch (err) {
    console.error(err);
    alert(err.message);
  }
}
