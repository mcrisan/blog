window.fbAsyncInit = function() {
        FB.init({appId: '793960300632535', status: true, cookie: true,
                 xfbml: true});
//        FB.Event.subscribe('auth.logout', function(response) {
//           window.location = "/logout";
//        });
        
        FB.Event.subscribe('auth.login', function(response) {
        	window.location = "/facebook_login";
          });
        
        FB.getLoginStatus(function(response) {
        	  if (response.status === 'connected') {
        		  $("#logout").on("click", function(event) {
        			  event.preventDefault();
        	    		FB.logout(function(response) {
        	    			window.location = "/logout";
        	    			});
        	    		
        		  }) 
        	    var uid = response.authResponse.userID;
        	    var accessToken = response.authResponse.accessToken;
        	  } else if (response.status === 'not_authorized') {
        	  } else {
        	    //alert("not con");
        	  }
        	 });
        
        
      };
      	
      
      
      (function() {
        var e = document.createElement('script');
        e.type = 'text/javascript';
        e.src = document.location.protocol + '//connect.facebook.net/en_US/all.js';
        e.async = true;
        document.getElementById('fb-root').appendChild(e);
      }());