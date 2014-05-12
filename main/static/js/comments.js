
$( document ).ready(function() {
$('.comments').on("click", '.reply',  function (event) {
	event.preventDefault();
	var parent_id = $(this).data('parentid');
	var post_id = $(this).data('postid');
    var item =  $(this).attr('href');
    var parent = $(this).parents(".comment").first();
    console.log($(this).length);
    if($(parent).find('textarea').length < 1) {
    	var textarea = $('<textarea>').attr({'class' : 'form-control', "required" : "true"});
    	var div = $('<div>').attr('class','col-xs-offset-3 col-lg-9').append($(textarea));
        var button = $('<button>').attr('class','btn btn-primary').text("Send");
        var div_button = $('<div>').attr('class','col-xs-offset-9 col-xs-10').append($(button));
        var div_container = $(parent).find('.form_container').first().append($(div)).append($(div_button));
    }else{
    	$(parent).find('textarea').remove();
      	$(parent).find('button').remove();
      	return;
    }
    $(button).click( function (event){
    	var text = $(parent).find('textarea').val();
    	if (text ==""){
    		$(parent).find(".error").text("You need to enter a message!");
    		return;
    	}
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
          		console.log($(parent).find(".error"));
          		$(parent).find(".error").text("You need o be logged in!");
          	}
            }
        });
    });
    		
 });
$('.comment').on("click", '.like',  function (event) {
	event.preventDefault();
	var mes = $(this).parents(".comment").first().find(".error");
	var id = $(this).data('id');
	$this = $(this);
	console.log(id);
	$.ajax({
        type: "POST",
        url: "/like_comment",
        data: { id_comment: id} ,
        cache: false,
        success: function(data) {
        	if (data !="-1"){
        		$($this).find("span").text(data['likes']);
        		$($this).parents("div").first().find(".unlike > span").text(data['unlikes']);
        		$(mes).text(data['mes']).show().delay(1000).fadeOut();
        	}else{
        		$(mes).text("You need to be logged in!").show().delay(2000).fadeOut();
        	}
        }
        });
    		
 });

$('.comment').on("click", '.unlike',  function (event) {
	event.preventDefault();
	var mes = $(this).parents(".comment").first().find(".error");
	var id = $(this).data('id');
	$this = $(this);
	console.log(id);
	$.ajax({
        type: "POST",
        url: "/unlike_comment",
        data: { id_comment: id} ,
        cache: false,
        success: function(data) {
        	if (data !="-1"){
        		$($this).find("span").text(data['unlikes']);
        		$($this).parents("div").first().find(".like > span").text(data['likes']);
        		$(mes).text(data['mes']).show().delay(1000).fadeOut();
        	}else{
        		$(mes).text("You need to be logged in!").show().delay(2000).fadeOut();
        	}
        }
        });
    		
 });


});