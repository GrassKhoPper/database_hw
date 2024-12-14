function toggleEditMode() {
  var gamesSection = document.getElementById('games-section');
  var editForm = document.getElementById('edit-form');
  if (gamesSection.style.display === 'none') {
    gamesSection.style.display = 'block';
    editForm.style.display = 'none';
  } else {
    gamesSection.style.display = 'none';
    editForm.style.display = 'block';
  }
}