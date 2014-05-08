$(function() {
	var search_data = [];		
	 $( "#autocomplete" ).autocomplete({
		 source: function( request, response ) {
			 $.ajax({
				 url: "/autocomplete",
				 dataType: "json",
				 data: {
				 term: request.term
				 },
				 success: function( data ) {
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
			 $("#search").trigger( "click" );
		 }
		 });
	
	
    });