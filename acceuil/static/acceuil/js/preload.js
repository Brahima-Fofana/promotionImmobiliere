window.onload = function () {
  const preloader = document.getElementById("preloader");
  const mainContent = document.getElementById("main-content");
  mainContent.style.display = "hidden";

  setTimeout(() => {
  preloader.style.display = "none";
  mainContent.style.display = "block";
  AOS.refresh();

    }, 300);

};
