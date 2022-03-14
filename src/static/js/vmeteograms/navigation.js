
// initiatlise
window.onload=initWebsite;

function initWebsite()
{
  var form = $("form");
  console.log('initWebsite')
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
  console.log('showPlot')
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
$("#change_date_id").change(changePlot);
// $(".js-change-plot").change(changePlot);

function changePlot() {
	var form = $(this).closest("form");
  console.log('changePlot')
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


// // select new location
// // $("#id_location").change(function () {
// $(".js-select-location").change(function () {
// 	var location = $(this).val();
// 	var form = $(this).closest("form");
//   console.log(form)
//   $.ajax({
//     // url: '/meteograms/ajax/select_location/',
// 	  url: form.attr("data-select-location-url"),
// 	  data: form.serialize(),
//     dataType: 'json',
//     success: function (data) {
//       if (data.is_taken) {
//         alert(data.error_message);
// 		  } else {
// 		      showPlot(form)
//       }
//     }
//   });
// });


// // select new date
// $(".js-select-date").change(function () {
// 	var date = $(this).val();
// 	var form = $(this).closest("form");
//   console.log('select-date')
//   $.ajax({
//     // url: '/meteograms/ajax/select_date/',
//    url: form.attr("data-select-date-url"),
//    data: form.serialize(),
//     dataType: 'json',
//     success: function (data) {
//       if (data.is_taken) {
//         alert(data.error_message);
//     } else {
//       showPlot(form)
//       }
//     }
//   });
// });


// // select new type
// $(".js-select-type").change(function () {
// 	var date = $(this).val();
// 	var form = $(this).closest("form");
//   console.log('select-type')
//   $.ajax({
//     // url: '/meteograms/ajax/select_type/',
//     url: form.attr("data-select-type-url"),
//     data: form.serialize(),
//     dataType: 'json',
//     success: function (data) {
//       if (data.is_taken) {
//         alert(data.error_message);
//     } else {
//       showPlot(form)
//       }
//     }
//   });
//
// });
