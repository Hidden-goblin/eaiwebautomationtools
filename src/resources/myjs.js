function() {
  var updateButton = document.getElementById('updateDetails');
  var favDialog = document.getElementById('favDialog');

  // “Update details” button opens the <dialog> modally
  updateButton.addEventListener('click', function() {
    favDialog.showModal();
  });
})();
