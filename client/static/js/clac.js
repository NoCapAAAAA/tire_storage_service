$(document).ready(function() {
  // Функция для обновления стоимости
  function updateCost() {
    var size = parseInt($('#id_size option:selected').text());
    var quantity = parseInt($('#id_quantity option:selected').text());
    var period = parseInt($('#id_period option:selected').text());
    var address = $('#id_adress option:selected').text();
    var cost;

    if (period * 30 > 30) {
      // Вычисление стоимости с условием period * 30 > 30
      cost = size * period * quantity / 1.5;
    } else if (period * 30 === 30) {
      // Вычисление стоимости с условием period * 30 = 30
      cost = size * period * quantity;
    } else {
      // Другое значение period
      // Здесь можно добавить обработку других условий, если необходимо
      cost = 0;
    }

    // Обновление отображения стоимости
    $('#summ').text(cost + ' руб');
  }

  // Обработчики событий для каждого select
  $('#id_size').change(function() {
    updateCost();
  });

  $('#id_quantity').change(function() {
    updateCost();
  });

  $('#id_period').change(function() {
    updateCost();
  });

  $('#id_adress').change(function() {
    updateCost();
  });
});
