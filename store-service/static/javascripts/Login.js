const loginButton = document.getElementById('loginButton');
const registerButton = document.getElementById('registerButton');
const loginForm = document.getElementById('login_form');
const registerForm = document.getElementById('register_form');
const Login_Registration_title = document.getElementById('Login/Registration');

const activeForm = document.body.dataset.activeForm;

if (activeForm === 'register') { 
	openRegisterForm();
} else {
	openLoginForm();
}
	
loginButton.addEventListener('click', openLoginForm);
	
registerButton.addEventListener('click', openRegisterForm);

function openRegisterForm() {
	registerButton.classList.add('active');
	loginButton.classList.remove('active');
	registerForm.style.display = 'block';
	loginForm.style.display = 'none';
	Login_Registration_title.textContent = 'Registration';
}

function openLoginForm() {
	loginButton.classList.add('active');
	registerButton.classList.remove('active');
	loginForm.style.display = 'block';
	registerForm.style.display = 'none';
	Login_Registration_title.textContent = 'Login';
}


