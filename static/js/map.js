let center = [53.22513774599916,44.923934130104676];

ymaps.ready(init);
  function init(){
  var myMap = new ymaps.Map("map", {
            center: center,

            zoom: 18
        });
    }


$('form').find('input').attr('autocomplete', 'off');