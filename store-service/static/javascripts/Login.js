const loginButton = document.getElementById('loginButton');
const registerButton = document.getElementById('registerButton');
const loginForm = document.getElementById('login_form');
const registerForm = document.getElementById('register_form');
const Login_Registration_title = document.getElementById('Login/Registration');

const activeForm = document.body.dataset.activeForm;

if (activeForm === 'register') {
	registerButton.classList.add('active');
	loginButton.classList.remove('active');
	registerForm.style.display = 'block';
	loginForm.style.display = 'none';
	Login_Registration_title.textContent = 'Registration';
} else {
	loginButton.classList.add('active');
	registerButton.classList.remove('active');
	loginForm.style.display = 'block';
	registerForm.style.display = 'none';
	Login_Registration_title.textContent = 'Login';
}

loginButton.addEventListener('click', () => {
	loginButton.classList.add('active');
	registerButton.classList.remove('active');
	loginForm.style.display = 'block';
	registerForm.style.display = 'none';
	Login_Registration_title.textContent = 'Login';
});

registerButton.addEventListener('click', () => {
	registerButton.classList.add('active');
	loginButton.classList.remove('active');
	registerForm.style.display = 'block';
	loginForm.style.display = 'none';
	Login_Registration_title.textContent = 'Registration';
});


