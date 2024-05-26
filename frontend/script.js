// Функция для отправки запроса на сервер
function sendData(url, data, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                callback(null, JSON.parse(xhr.responseText));
            } else {
                callback(xhr.status);
            }
        }
    };
    xhr.send(JSON.stringify(data));
}

// Функция для обработки отправки формы логина
function login(event) {
    event.preventDefault();
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var data = { "login": username, "password": password };
    sendData("/login", data, function(err, result) {
        if (err) {
            document.getElementById("message").textContent = "Error: " + err;
        } else {
            if (result.error) {
                document.getElementById("message").textContent = result.error;
            } else {
                document.getElementById("message").textContent = result.message;
                // Перенаправление на другую страницу или выполнение других действий после успешного входа
            }
        }
    });
}

// Функция для обработки отправки формы регистрации
function register(event) {
    event.preventDefault();
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var data = { "login": username, "password": password };
    sendData("/register", data, function(err, result) {
        if (err) {
            document.getElementById("message").textContent = "Error: " + err;
        } else {
            if (result.error) {
                document.getElementById("message").textContent = result.error;
            } else {
                document.getElementById("message").textContent = result.message;
                // Перенаправление на другую страницу или выполнение других действий после успешной регистрации
            }
        }
    });
}

// Привязка обработчиков событий к формам
document.getElementById("loginForm").addEventListener("submit", login);
document.getElementById("registerForm").addEventListener("submit", register);
