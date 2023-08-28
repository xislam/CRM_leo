
document.addEventListener('DOMContentLoaded', function () {
  var modal = document.getElementById('mailingModal');
  var buttons = document.getElementsByClassName('mailing-button');
  var form = document.getElementById('mailingForm');
  var closeButton = document.getElementsByClassName('close')[0];

  for (var i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener('click', function () {
      modal.style.display = 'block';
    });
  }

  closeButton.addEventListener('click', function () {
    modal.style.display = 'none';
  });

  window.addEventListener('click', function (event) {
    if (event.target === modal) {
      modal.style.display = 'none';
    }
  });

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    var title = document.getElementById('title').value;
    var message = document.getElementById('message').value;

    // Отправка данных формы на сервер (можно использовать AJAX)

    // После успешной отправки закройте модальное окно
    modal.style.display = 'none';
  });
});