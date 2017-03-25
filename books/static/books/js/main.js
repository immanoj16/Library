/**
 * Created by KANHU on 15-03-2017.
 */

$('ul.nav li.dropdown').hover(function() {
  $(this).find('.dropdown-menu').stop(true, true).delay(100).fadeIn(100);
  }, function() {
  $(this).find('.dropdown-menu').stop(true, true).delay(100).fadeOut(100);
});
