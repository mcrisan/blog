$( document ).ready(function() {
        $.ajax({
        type: "POST",
        url: "/featured_posts",
        cache: false,
        success: function(data) {
        	console.log(data);
        	$.each(data['slider'], function(index, value) {
        		console.log(value['name']);

				});
        	var slider = new newSlider('#a', data);
            slider.createElem();
            }
        });
})

/**
 * Class in which the slider element will be created
 * 
 * @name newSlider
 * @param {String} id - id of the element where the slider will be inserted
 * @param {JSON} elem - the elements of the slider
 */
function newSlider(id, elem) {

    /**
     * The element in which the slider will be created
     *
     * @type Object
     * @memberof newSlider
     */
    this.element = $(id);

    /**
     * The JSON received as parameter
     *
     * @type JSON
     * @memberof newSlider
     */
    this.elem = elem;

    /**
     * Keep a reference to the newSlider object
     *
     * @type Object
     * @memberof newSlider
     */
    var $this = this;

    /**
     * Call the functions to create the elements of he slider
     * 
     * @memberof newSlider
     */
    this.createElem = function() {
        $this.createDiv();
        $this.createPictureNav();
        $this.clickEvent();
    };

    /**
     * Creates a div for navigating through images 
     * and a div to display the image
     * 
     * @memberof newSlider
     */
    this.createDiv = function() {
        $this.divNav = $('<div/>').appendTo($this.element);
        $this.divNav.addClass("nav");
        $this.divImg = $('<div/>').prependTo($this.element);
    };

    /**
     * Creates multiple div's, with the data red from the JSON.
     * The divs will be used to navigate through all the images.
     * This function will also display the first image
     * 
     * @memberof newSlider
     */
    this.createPictureNav = function() {
        //var obj = jQuery.parseJSON($this.elem);
        $.each(this.elem['slider'], function(index, value) {
            var src = value['src'];
            var name = value['name'];
            var link = value['link'];
            if (0 === index) {
                $this.createBigImg(src, name, link);
            }
            var nav = $('<div/>', {class: "smalldiv"}).appendTo($this.divNav);
            nav.attr("data-src", src);
            nav.attr("data-name", name);
            nav.attr("data-link", link);
        });
    };

    /**
     * Function used to create all the click events
     * necessary
     * 
     * @name clickEvent
     * @memberof newSlider
     */
    this.clickEvent = function() {
        $this.element.find(".smalldiv").click(function() {
            var src = $(this).data("src");
            var name = $(this).data("name");
            var link = $(this).data("link");
            $this.removeElemClass();
            $(this).addClass('focus');
            $this.createBigImg(src, name, link);
        }
        );
    };

    /**
     * Function used to remove class for navigation divs
     * 
     * @name removeElemClass
     * @memberof newSlider
     */
    this.removeElemClass = function() {
        var nav = $this.divNav.find(".smalldiv");
        $.each(nav, function(index, value) {
            $(value).removeClass('focus');
        });
    };


    /**
     * Creates the image and text for the selected element.
     * 
     * @name createBigImg
     * @param {String} src - Src attribute of the image.
     * @param {String} name - The text to display
     * @param {String} link - The link of the text
     * @memberof newSlider
     */
    this.createBigImg = function(src, name, link) {
        var image = $('<img/>', {src: src, class: "bigimg img-responsive"});
        $($this.divImg).html(image);
        var text = $('<a/>', {href: link, text: name, class: "text"});
        $($this.divImg).append(text);
        $(text).addClass("text");

    };
}
