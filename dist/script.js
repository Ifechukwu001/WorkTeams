// Get Current Year

const currentYear = document.getElementById("currentYear")
let date = new Date()
let year = date.getFullYear()

currentYear.innerHTML = year

document.getElementById('signup').addEventListener('click', () =>{
  const userEmail = document.getElementById('email').value
  const userPassword = document.getElementById('password').value

  
  fetch('https://ifechukwu.pythonanywhere.com/api/user', {
    method: 'POST',
    body: JSON.stringify({
      email: userEmail,
      password: userPassword
    }),
    headers: {
      'Content-Type': 'application/json'
    }
  })

  fetch('https://ifechukwu.pythonanywhere.com/api/user')
    .then(response => response.json())
    .then(data => console.log(data)) 

})

