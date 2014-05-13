
$( document ).ready(function() {
	$("#fb-login").on("click", function(){
		FB.login(function(response) {
			if (response.status === 'connected') {
				  $.ajax({
				        type: "POST",
				        url: "/facebook_login",
				        cache: false,
				        success: function(data) {
				        	window.location = "/"
				        	console.log("logat");
				        }
				        });  
		    } else if (response.status === 'not_authorized') {
		      window.location = "/login"
		    } else {
		    	window.location = "/login"
		    }
			}, {scope: 'email,user_birthday, manage_pages'});;
	})
})



function statusChangeCallback(response) {
    if (response.status === 'connected') {
		  $.ajax({
		        type: "POST",
		        url: "/facebook_login",
		        cache: false,
		        success: function(data) {
		        	window.location = "/"
		        	console.log("logat");
		        }
		        });  
    } else if (response.status === 'not_authorized') {
      window.location = "/login"
      document.getElementById('status').innerHTML = 'Please log ' +
        'into this app.';
    } else {
    	window.location = "/login"
      document.getElementById('status').innerHTML = 'Please log ' +
        'into Facebook.';
    }
  }


function checkLoginState() {
    FB.getLoginStatus(function(response) {
      statusChangeCallback(response);
    });
  }


window.fbAsyncInit = function() {
        FB.init({appId: '793960300632535', 
        		 status: true, 
        		 cookie: true,
                 xfbml: true
                 });
        
        FB.getLoginStatus(function(response) {
            //statusChangeCallback(response);
          });
               
      };
      	
      
      
      (function() {
        var e = document.createElement('script');
        e.type = 'text/javascript';
        e.src = document.location.protocol + '//connect.facebook.net/en_US/all.js';
        e.async = true;
        document.getElementById('fb-root').appendChild(e);
      }());