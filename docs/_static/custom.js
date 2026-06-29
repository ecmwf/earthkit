document.addEventListener("DOMContentLoaded", function () {
  // Packages list is injected at build time from earthkit-packages.yml via earthkit-packages.js
  var packages = window.earthkitPackages || [];
  if (!packages.length) return;

  // Build the <select> from the YAML-derived packages list
  var select = document.createElement("select");
  select.setAttribute("aria-label", "Select earthkit documentation");

  // Placeholder option
  var placeholder = document.createElement("option");
  placeholder.value = "";
  placeholder.textContent = "Explore the earthkit ecosystem";
  placeholder.disabled = true;
  placeholder.selected = true;
  select.appendChild(placeholder);

  packages.forEach(function (p) {
    var opt = document.createElement("option");
    opt.value = p.url;
    opt.textContent = p.name;
    select.appendChild(opt);
  });

  // Navigate immediately on selection
  select.addEventListener("change", function () {
    var url = select.value;
    if (url) {
      window.location.href = url;
      select.value = "";
    }
  });

  // Wrapper div
  var wrapper = document.createElement("div");
  wrapper.className = "ek-project-selector";
  wrapper.appendChild(select);

  // Mount into the brand placeholder above the search bar
  var mount = document.getElementById("ek-project-selector-mount");
  if (mount) {
    mount.appendChild(wrapper);
  }
});
