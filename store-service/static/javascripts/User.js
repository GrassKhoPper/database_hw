document.addEventListener('DOMContentLoaded', function () {
  // File-upload-label change text
  const fileInput = document.getElementById('profile-avatar');
  const fileLabel = document.querySelector('.file-upload-label');

  fileInput.addEventListener('change', function() {
    if (fileInput.files.length > 0) {
       fileLabel.textContent = fileInput.files[0].name
    } else {
        fileLabel.textContent = 'Click for download image'
    }
  });

  // Change forms
  const formButton = document.querySelectorAll('.button_form');
  const forms = document.querySelectorAll('.form');  
  
  function showForm(formId) {
    forms.forEach(form => {
      form.classList.remove('active');
      if (form.id === formId) {
        form.classList.add('active');
      }
    });
  }

  function setActiveButton(button) {
    formButton.forEach(btn => btn.classList.remove('active'));
      button.classList.add('active');
  }

  formButton.forEach(button => {
    button.addEventListener('click', function () {
      const formId = this.getAttribute('data-form');
      showForm(formId);
      setActiveButton(this);
    });
  });

  const activeForm = document.querySelector('.form.active');
  if (activeForm) {
    const activeBtn = document.querySelector(`[data-form="${activeForm.id}"]`);
    setActiveButton(activeBtn);
  }
});

function check_int(value) {
  value = Math.max(0, Math.min(2147483647 , parseInt(value)));
  return isNaN(value) ? 0 : value;;
}

document.addEventListener('DOMContentLoaded', function() {



});