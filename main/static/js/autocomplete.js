$(function() {
	var search_data = [];	
	var data2 =[]
	 $( "#autocomplete" ).autocomplete({
		 source: function( request, response ) {
			 $.ajax({
				 url: "/autocomplete",
				 dataType: "json",
				 data: {
				 term: request.term
				 },
				 success: function( data ) {
					 data2 = data;
					 $.each(data['posts'], function(index, value) {
						  search_data[index] = value['title']
						});
					 response(search_data);
				 },
			 	});
			 },
		 minLength: 1,
		 select: function( event, ui ) {
			 $("#autocomplete").val(ui.item.label);
			 console.log(data2);
			 var id="";
			 $.each(data2['posts'], function(index, value) {
				  if (ui.item.label == value['title']){
					  id = value['id'];
					  location.href = "/post/"+id;
					  return;
				  }
				});
			 //$("#search").trigger( "click" );
		 }
		 });
	
	
    });