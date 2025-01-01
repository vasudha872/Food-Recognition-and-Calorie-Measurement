const form = document.querySelector('form');
form.addEventListener('submit', async (event) => {
  event.preventDefault();  // prevent the default form submission

  // Get the username and password from the form inputs
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  // Send a POST request to the server-side script to authenticate the user
  const response = await fetch('/auth', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      username: username,
      password: password
    })
  });

  // If the authentication is successful, redirect the user to the food recognition page
  if (response.ok) {
    window.location.href = '/food.html';
  } else {
    // Otherwise, display an error message
    const errorMessage = document.createElement('p');
    errorMessage.textContent = 'Incorrect username or password';
    form.appendChild(errorMessage);
  }
});

// Authentication middleware
function requireAuth(req, res, next) {
    if (req.session && req.session.loggedIn) {
      next();
    } else {
      res.redirect('/login.html');
    }
  }
  
  // Route for the food recognition page
  app.get('/food.html', requireAuth, (req, res) => {
    // Render the food recognition page
    res.render('food');
  });
  
