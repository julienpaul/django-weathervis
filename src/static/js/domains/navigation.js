
// change campaign
$("#change_campaign_id").change(changeCampaign);

function changeCampaign() {
  console.log('chaneCampaign')
  var form = $(this).closest("form");
  $.ajax({
	  url: form.attr("data-change-campaign-url"),
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
