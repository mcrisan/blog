
$( document ).ready(function() {
//$('.reply').click( function (event) {
$('.comments').on("click", '.reply',  function (event) {
	event.preventDefault();
	var parent_id = $(this).data('parentid');
	var post_id = $(this).data('postid');
    var item =  $(this).attr('href');
    var parent = $(this).parents(".comment").first();
    console.log($(this).length);
    if($(parent).find('textarea').length < 1) {
    	var textarea = $('<textarea>').attr('class','form-control');
    	var div = $('<div>').attr('class','col-xs-offset-3 col-lg-9').append($(textarea));
        var button = $('<button>').attr('class','btn btn-primary').text("Send");
        var div_button = $('<div>').attr('class','col-xs-offset-9 col-xs-10').append($(button));
        var div_container = $(parent).find('.form_container').first().append($(div)).append($(div_button));
        //$(parent).append($(div_container));
    }else{
    	$(parent).find('textarea').remove();
      	$(parent).find('button').remove();
      	return;
    }
    $(button).click( function (event){
    	var text = $(parent).find('textarea').val();
        $.ajax({
        type: "POST",
        url: "/create_comment",
        data: { id_post: post_id, id_parent : parent_id, text : text} ,
        cache: false,
        success: function(data) {
          	$(textarea).remove();
          	$(button).remove();
          	if (data !="-1"){
          		$(parent).append(data);  
          	}else{
          		div = $('<div>').attr('class','flashes col-xs-offset-3 col-xs-9').text("You need o be logged in!");
          		$(parent).append($(div));
          	}
            }
        });
    });
    		
 });

$('.like').click( function (event) {
	event.preventDefault();
    		
 });


});