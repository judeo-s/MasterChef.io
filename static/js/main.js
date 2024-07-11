function displayFlashMessage(category, message) {
    const flashesDiv = document.getElementById('flashes');
    const flashDiv = document.createElement('div');
    flashDiv.className = 'flash ' + category;
    flashDiv.innerText = message;
    flashesDiv.appendChild(flashDiv);
    setTimeout(() => {
      flashDiv.remove();
    }, 5000);
  }


  document.addEventListener('DOMContentLoaded', function() {
    const viewButtons = document.querySelectorAll('.view-recipe');
    const deleteButtons = document.querySelectorAll('.delete-recipe');
    const modal = document.getElementById('recipeModal');
    const confirmationModal = document.getElementById('confirmationModal');
    const closeButtons = document.querySelectorAll('.close');
    const confirmDeleteButton = document.getElementById('confirmDelete');
    let currentDeleteForm = null;
  
    // View Recipe Modal
    viewButtons.forEach(button => {
      button.addEventListener('click', function() {
        const recipeId = this.getAttribute('data-recipe-id');
        fetch(`/recipe/${recipeId}`)
          .then(response => response.json())
          .then(data => {
            document.getElementById('recipe-title').textContent = data.title;
            document.getElementById('recipe-image').src = data.image_url;
            document.getElementById('recipe-description').textContent = data.description;
            const ingredientsList = document.getElementById('recipe-ingredients');
            ingredientsList.innerHTML = '';
            data.ingredients.split(',').forEach(ingredient => {
              const li = document.createElement('li');
              li.textContent = ingredient;
              ingredientsList.appendChild(li);
            });
            document.getElementById('recipe-instructions').href = data.instructions;
            modal.style.display = 'block';
          });
      });
    });
  
    // Delete Confirmation Modal
    deleteButtons.forEach(button => {
      button.addEventListener('click', function() {
        currentDeleteForm = this.closest('form');
        confirmationModal.style.display = 'block';
      });
    });
  
    confirmDeleteButton.addEventListener('click', function() {
      if (currentDeleteForm) {
        currentDeleteForm.submit();
      }
    });
  
    // Close Modal
    closeButtons.forEach(button => {
      button.addEventListener('click', function() {
        modal.style.display = 'none';
        confirmationModal.style.display = 'none';
      });
    });
  
    window.addEventListener('click', function(event) {
      if (event.target == modal) {
        modal.style.display = 'none';
      }
      if (event.target == confirmationModal) {
        confirmationModal.style.display = 'none';
      }
    });
  });
  