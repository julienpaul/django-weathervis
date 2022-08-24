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
  $('.list-group').animate({scrollTop: aTag.offset().top - 200},'slow');
}

function highlight(aslug) {
  // animate marker
  bounce_marker(aslug);
  // animate domain
  highlight_domain(aslug);
}
