/* Project specific Javascript goes here. */

// window.addEventListener('load', function () {
$(document).ready(function (e) {
  // show active anchor card, on load
  if (document.getElementById('id_slug')) {
    const slug = document.getElementById('id_slug').value;
    const id = 'list-'+slug+'-list';

    $($('#'+id).get(0)).tab('show');
    scroll_to_anchor(id);
  }
  // show active anchor card, on click
  $(".list-group a").click(function (event) {
    const aslug = $(this).attr('id').split("-")[1];
    highlight(aslug);
    $(this).tab('show');
  });
});

function scroll_to_anchor(aid){
  // scroll down to active anchor
  var aTag = $("a[id='"+ aid +"']");
  $('.list-group').animate({scrollTop: aTag.offset().top - 250},'slow');
}

function highlight(aslug) {
  // animate marker
  bounce_marker(aslug);
  // animate domain
  highlight_domain(aslug);
}

/* to make messages disappear */
// Get all info messages
var info_messages = document.getElementsByClassName('alert-info');
setTimeout(function(){
    for (var i = 0; i < info_messages.length; i ++) {
        // Set display attribute as !important, neccessary when using bootstrap
        info_messages[i].setAttribute('style', 'display:none !important');
    }
}, 3000);

var success_messages = document.getElementsByClassName('alert-success');
setTimeout(function(){
    for (var i = 0; i < success_messages.length; i ++) {
        // Set display attribute as !important, neccessary when using bootstrap
        success_messages[i].setAttribute('style', 'display:none !important');
    }
}, 4000);
