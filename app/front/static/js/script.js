document.addEventListener("DOMContentLoaded", function() {
  $('.main-content').animate({'opacity': 1},300);
});

$('#registerForm').submit(function(event) {
  event.preventDefault(); // Предотвращаем стандартное поведение формы

  // Получаем данные из формы
  var username = $('#registerUsername').val();
  var email = $('#registerEmail').val();
  var password = $('#registerPassword').val();

  // Отправляем данные на сервер
  $.ajax({
      url: '/register',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({
          username: username,
          email: email,
          password: password,
      }),
      success: function(response) {
          // Если регистрация прошла успешно, перенаправляем пользователя на другую страницу
          window.location.href = '/authorization';
      },
      error: function(xhr, textStatus, errorThrown) {
          // Если произошла ошибка при регистрации, отображаем сообщение об ошибке
          console.error(xhr.responseText);
          alert('Ошибка при регистрации: ' + xhr.responseText);
      }
  });
});

$(document).ready(function() {
  $('#loginForm').submit(function(event) {
      event.preventDefault(); // Предотвращаем стандартное поведение формы

      // Получаем данные из формы
      var email = $('#loginEmail').val();
      var password = $('#loginPassword').val();

      // Отправляем данные на сервер
      $.ajax({
          url: '/login', 
          type: 'POST',
          contentType: 'application/json',
          data: JSON.stringify({
              email: email,
              password: password
          }),
          success: function(response) {
              // Проверяем тип пользователя
              if (response.role === "admin") {
                  // Разрешаем доступ к странице 
                  window.location.href = '/profile/';
              } else {
                  // Разрешаем доступ к обычной странице 
                  window.location.href = '/profile/';
              }
          },
          error: function(xhr, textStatus, errorThrown) {
              // Если произошла ошибка при входе, отображаем сообщение об ошибке
              console.error(xhr.responseText);
              alert('Ошибка при входе: ' + xhr.responseText);
          }
      });
  })
});

$('#messageBox').submit(function(event) {
  event.preventDefault(); // Предотвращаем стандартное поведение формы

  // Получаем данные из формы
  var message = $('#userMessage').val();

  // Отправляем данные на сервер
  $.ajax({
      url: '/send', // URL вашего эндпоинта FastAPI для регистрации
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({
          message: message,
      }),
      success: function(response) {
          window.location.reload();
      },
      error: function(xhr, textStatus, errorThrown) {
          // Если произошла ошибка при регистрации, отображаем сообщение об ошибке
          console.error(xhr.responseText);
          alert('Ошибка при отправке: ' + xhr.responseText);
      }
  });
});

function set_color(value){
    if (value <= 40) {
      return "#6eec2a";
    }
    if ((value > 40) && (value <= 70)) {
      return "#ece92a";
    }
    if ((value > 70) && (value <= 100)) {
      return "#ec952a";
    }
    if (value > 100) {
      return "#d9302f";
    }
}

function set_advice(value) {
    if (value <= 40) {
      return "Вдохните поглубже!";
      }
    if ((value <= 90) && (value > 40)) {
      return "Долго не гуляйте";
    }
    if (value > 90) {
      return "Лучше остаться дома";
    }
}

async function updateClass() {
    const response = await fetch(`/get_value?nocache=${new Date().getTime()}`, {
      headers: { "Cache-Control": "no-cache, no-store, must-revalidate" }
    });
    const data = await response.json();
    const dataArray = Object.values(data?.data || {}).map(item => Array.isArray(item) ? item : Object.values(item));

    let element = document.getElementById(0);
    element.style.backgroundColor = set_color(dataArray[0][0]['mean AQI']);
    element.textContent = dataArray[0][0]['mean AQI']+"\nAQI";

    let element_advice = document.getElementsByClassName("advice-text");
    element_advice[1].textContent = set_advice(dataArray[0][0]['mean AQI']);

    for (let i = 1; i < 7; i++) {
      let element = document.getElementById(i);
      child1 = element.children[0].children[1];
      child2 = element.children[1].children[1];
      child3 = element.children[2].children[1];

      child1.textContent = dataArray[0][i]['date'];
      child2.textContent = dataArray[0][i]['mean AQI']+"\nAQI";
      child2.style.backgroundColor = set_color(dataArray[0][i]['mean AQI']);
      child3.textContent = dataArray[0][i]['message'];
    }
    console.log("Данные обновлены");
  }
window.onload = updateClass;

