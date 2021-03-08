document.onreadystatechange = function () {
  if (document.readyState == "complete") {
    const updateButton = document.getElementById('updateDetails');

updateButton.addEventListener('click', function() {
    var favDialog = document.getElementById('favDialog');
    if (typeof favDialog.showModal === "function") {
      favDialog.showModal();
    } else {
//     Do something else
      console.error("L'API dialog n'est pas prise en charge par votre navigateur");
    }

  });
  }
}
