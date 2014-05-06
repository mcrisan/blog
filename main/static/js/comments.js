
$( document ).ready(function() {
$('.reply').click( function (event) {
	event.preventDefault();
	var parent_id = $(this).data('parentid');
	var post_id = $(this).data('postid');
    var item =  $(this).attr('href');
    if($(this).parent().find('textarea').length < 1) {
        $(this).parent().append($('<textarea>').attr('class','reply'));
    } else {
        var textarea = $(this).parent().find('textarea');
        var text = $(this).parent().find('textarea').val();
        var parent = $(this).parent();
        $.ajax({
            type: "POST",
            url: "/create_comment",
            data: { id_post: post_id, id_parent : parent_id, text : text} ,
            cache: false,
            success: function(data) {
            	$(textarea).remove();
            	$(parent).append(data);
                
            }
        });
    }
 });
});