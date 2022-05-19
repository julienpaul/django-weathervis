
// initiatlise
window.onload=initWebsite;

function initWebsite()
{
  var form = $("form");
  $.ajax({
  // url: '/meteograms/ajax/select_location/',
	// url: form.attr("data-select-location-url"),
	url: form.attr("data-change-plot-url"),
	data: form.serialize(),
  dataType: 'json',
  success: function (data) {
  if (data.is_taken) {
    alert(data.error_message);
  } else {
		showPlot(form)
      }
    }
  });
}

// show plot
function showPlot(form)
{
  $.ajax({
    // url: '/meteograms/ajax/switch_plot/',
    url: form.attr("data-show-plot-url"),
    data: form.serialize(),
    dataType: 'json',
    success: function (data) {
      if (data.is_taken) {
        alert(data.error_message);
      } else {
        document.getElementById("panel1").src=data.img1.url;
        document.getElementById("panel1").alt=data.img1.nam;
        // document.getElementById("title1").innerHTML=data.img1.ttl;
        document.getElementById("panel2").src=data.img2.url;
        document.getElementById("panel2").alt=data.img2.nam;
        // document.getElementById("title2").innerHTML=data.img2.ttl;
      }
    }
  });
}

// change plot
// $("#change-plot_id").on('change', changePlot());
$("#change_location_id").change(changePlot);
$("#change_points_id").change(changePlot);
$("#change_date_id").change(changePlot);
// $(".js-change-plot").change(changePlot);

function changePlot() {
	var form = $(this).closest("form");
  $.ajax({
    // url: '/meteograms/ajax/select_location/',
	  url: form.attr("data-change-plot-url"),
	  data: form.serialize(),
    dataType: 'json',
    success: function (data) {
      if (data.is_taken) {
        alert(data.error_message);
		  } else {
        window.location.replace(data.url)
      }
    }
  });
}
