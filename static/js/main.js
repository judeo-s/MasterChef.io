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