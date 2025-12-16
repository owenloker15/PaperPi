document.addEventListener("DOMContentLoaded", () => {
  const slideshowInput = document.getElementById("slideshow-input");
  const slideshowGrid = document.getElementById("slideshow-grid");
  const dropzone = document.getElementById("slideshow-dropzone");

  if (!dropzone || !slideshowInput || !slideshowGrid) return;

  // Track all selected files
  let selectedFiles = [];

  // -------------------- Drag & drop --------------------
  dropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.classList.add("dragover");
  });

  dropzone.addEventListener("dragleave", (e) => {
    e.preventDefault();
    dropzone.classList.remove("dragover");
  });

  dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("dragover");

    const files = Array.from(e.dataTransfer.files).filter((f) =>
      f.type.startsWith("image/"),
    );
    addFiles(files);
  });

  // -------------------- File input --------------------
  slideshowInput.addEventListener("change", () => {
    const files = Array.from(slideshowInput.files).filter((f) =>
      f.type.startsWith("image/"),
    );
    addFiles(files);
  });

  // -------------------- Add files & preview --------------------
  function addFiles(files) {
    files.forEach((file) => {
      // Avoid duplicates
      if (
        !selectedFiles.some((f) => f.name === file.name && f.size === file.size)
      ) {
        selectedFiles.push(file);
        addPreview(file);
      }
    });
    updateFileInput();
  }

  // -------------------- Preview tile --------------------
  function addPreview(file) {
    const tile = document.createElement("div");
    tile.className = "slideshow-tile";
    tile.dataset.name = file.name;

    const img = document.createElement("img");
    img.src = URL.createObjectURL(file);
    tile.appendChild(img);

    const btn = document.createElement("button");
    btn.innerText = "✕";
    btn.title = "Remove";
    btn.onclick = () => removeFile(file, tile);
    tile.appendChild(btn);

    slideshowGrid.appendChild(tile);
  }

  // -------------------- Remove file --------------------
  function removeFile(file, tile) {
    selectedFiles = selectedFiles.filter((f) => f !== file);
    tile.remove();
    updateFileInput();
  }

  // -------------------- Sync files with input so FormData works --------------------
  function updateFileInput() {
    const dataTransfer = new DataTransfer();
    selectedFiles.forEach((f) => dataTransfer.items.add(f));
    slideshowInput.files = dataTransfer.files;
  }
});
