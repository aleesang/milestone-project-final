$(document).ready(function() {

/* parallax */
var rellax = new Rellax('.rellax', {
    speed: -2,
    center: false,
    wrapper: null,
    round: true,
    vertical: true,
    horizontal: false
  });

/* toasts */
$('.toast').toast('show');

});
