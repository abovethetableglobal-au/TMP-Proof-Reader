// TMP Check portal — navigation toggle and upload validation.
(function () {
  "use strict";

  // Off-canvas navigation (mobile)
  document.querySelectorAll("[data-nav-open]").forEach(function (b) {
    b.addEventListener("click", function () { document.body.classList.add("nav-open"); });
  });
  document.querySelectorAll("[data-nav-close]").forEach(function (b) {
    b.addEventListener("click", function () { document.body.classList.remove("nav-open"); });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") document.body.classList.remove("nav-open");
  });

  function fmtSize(n) {
    return n < 1048576 ? (n / 1024).toFixed(0) + " KB" : (n / 1048576).toFixed(1) + " MB";
  }

  // Basic signature check so a renamed file is caught before upload.
  // PDF starts with "%PDF-"; DOCX is a ZIP container ("PK\x03\x04").
  function sniff(file) {
    return file.slice(0, 5).arrayBuffer().then(function (buf) {
      var b = new Uint8Array(buf);
      if (b[0] === 0x25 && b[1] === 0x50 && b[2] === 0x44 && b[3] === 0x46) return ".pdf";
      if (b[0] === 0x50 && b[1] === 0x4b && b[2] === 0x03 && b[3] === 0x04) return ".docx";
      return null;
    });
  }

  document.querySelectorAll("[data-dropzone]").forEach(function (zone) {
    var input = zone.querySelector("input[type=file]");
    var status = zone.querySelector(".dz-status");
    var nameEl = zone.querySelector(".dz-name");
    var sizeEl = zone.querySelector(".dz-size");
    var msg = zone.querySelector(".dz-msg");
    var bar = zone.querySelector(".progress span");
    var maxBytes = parseInt(zone.dataset.maxBytes, 10);
    var allowed = zone.dataset.allowed.split(",");

    function show(file, tone, text) {
      status.hidden = false;
      status.className = "dz-status " + (tone || "");
      nameEl.textContent = file ? file.name : "";
      sizeEl.textContent = file ? fmtSize(file.size) : "";
      msg.textContent = text;
      bar.style.width = tone === "ok" ? "100%" : "0";
    }

    function handle(file) {
      if (!file) return;
      var ext = (file.name.match(/\.[^.]+$/) || [""])[0].toLowerCase();
      if (allowed.indexOf(ext) === -1) {
        return show(file, "error", "This file type is not supported. Upload a PDF or Word (.docx) file. Older .doc files must be saved as .docx first.");
      }
      if (file.size === 0) return show(file, "error", "This file is empty. Check the file and try again.");
      if (file.size > maxBytes) {
        return show(file, "error", "This file is " + fmtSize(file.size) + ". The maximum size is " + fmtSize(maxBytes) + ".");
      }
      sniff(file).then(function (kind) {
        if (kind !== ext) {
          return show(file, "error", "This file does not appear to be a valid " + ext.slice(1).toUpperCase() + " document. It may be damaged or renamed.");
        }
        show(file, "ok", "File checks passed. Sending files to the checking service is not yet connected in this version — no credit has been used.");
      });
    }

    input.addEventListener("change", function () { handle(input.files[0]); });
    ["dragenter", "dragover"].forEach(function (ev) {
      zone.addEventListener(ev, function (e) { e.preventDefault(); zone.classList.add("drag"); });
    });
    ["dragleave", "drop"].forEach(function (ev) {
      zone.addEventListener(ev, function (e) { e.preventDefault(); zone.classList.remove("drag"); });
    });
    zone.addEventListener("drop", function (e) {
      var files = e.dataTransfer.files;
      if (files.length > 1) return show(null, "error", "Upload one TMP package at a time.");
      handle(files[0]);
    });
  });
})();
