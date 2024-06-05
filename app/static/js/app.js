const closeIcons = document.querySelectorAll(".flash-close");
closeIcons.forEach((icon) => {
  icon.onclick = function () {
    this.parentElement.style.display = "none";
  };
});
