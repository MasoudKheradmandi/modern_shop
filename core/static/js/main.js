(function ($) {
    "use strict";

    /*-------------------------------------
    Animated Headline
    -------------------------------------*/
    if ($.fn.animatedHeadline !== undefined && $(".ah-animate").length) {
        var target_slider = $(".ah-animate"),
            ah_options = target_slider.data('line-options');
        if (typeof ah_options === "object") {
            target_slider.animatedHeadline(ah_options);
        }
    }
  
   /*-------------------------------------
    Youtube Video
    -------------------------------------*/   
    if ($.fn.YTPlayer !== undefined && $("#fxtVideo").length) { 
        $("#fxtVideo").YTPlayer({useOnMobile:true});
    }  
      
    /*-------------------------------------
    Gallery Popup
    -------------------------------------*/

    if ($('#project-wrapper').length) {
        $('#project-wrapper').magnificPopup({
            type: 'image',
            delegate: 'a.zoom',
            gallery: {
                enabled: true
            }
        });
    }

    /*-------------------------------------
    Sidebar
    -------------------------------------*/
    if ($(window).width() > 991) {
        $('.btn-toggle').on('click', function () {
            if ($("body").hasClass('open-sidebar')) {
                $('.fxt-page-content').find('.active-animation').each(function () {
                    $(this).removeClass('active-animation');
                });
            } else {
                runObserver();
            }
            $("body").toggleClass("open-sidebar");
        });
    }

    /*-------------------------------------
    On Load
    -------------------------------------*/
    $(window).on('load resize', function () {

        $('body').imagesLoaded().done(function (instance) {
            $('body').addClass('loaded');
        });

        $('[data-type="section-switch"], #triger-page-content').on('click', function () {
            if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
                var target = $(this.hash);
                if (target.length > 0) {

                    target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
                    $('html,body').animate({
                        scrollTop: target.offset().top
                    }, 1000);
                    return false;
                }
            }
        });

    });

    /*-------------------------------------
    Intersection Observer
    -------------------------------------*/
    function runObserver() {
        if (!!window.IntersectionObserver) {
            let observer = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("active-animation");
                        observer.unobserve(entry.target);
                    }
                });
            }, {
                rootMargin: "0px 0px -150px 0px"
            });
            document.querySelectorAll('.has-animation').forEach(block => {
                observer.observe(block)
            });
        } else {
            document.querySelectorAll('.has-animation').forEach(block => {
                block.classList.remove('has-animation')
            });
        }
    }

    runObserver();

    /*-------------------------------------
	Section background image
	-------------------------------------*/
    $("[data-bg-image]").each(function () {
        var img = $(this).data("bg-image");
        $(this).css({
            backgroundImage: "url(" + img + ")"
        });
    });

    /*-------------------------------------
    Vegas Slider
    -------------------------------------*/
    if ($.fn.vegas !== undefined && $("#vegas-slide").length) {
        var target_slider = $("#vegas-slide"),
            vegas_options = target_slider.data('vegas-options');
        if (typeof vegas_options === "object") {
            target_slider.vegas(vegas_options);
        }
    }

    /*-------------------------------------
    Subscribe Form Activation
    -------------------------------------*/
    $('[data-pixsaas]').each(function () {
        var $this = $(this);
        $('.form-result', $this).css('display', 'none');

        $this.submit(function () {

            $('button[type="submit"]', $this).addClass('clicked');

            // Create a object and assign all fields name and value.
            var values = {};

            $('[name]', $this).each(function () {
                var $this = $(this),
                    $name = $this.attr('name'),
                    $value = $this.val();
                values[$name] = $value;
            });

            // Make Request
            $.ajax({
                url: $this.attr('action'),
                type: 'POST',
                data: values,
                success: function success(data) {

                    if (data.error == true) {
                        $('.form-result', $this).addClass('alert-warning').removeClass('alert-success alert-danger').fadeIn(200).show().fadeOut(50000);
                    } else {
                        $('.form-result', $this).addClass('alert-success').removeClass('alert-warning alert-danger').fadeIn(200).show().fadeOut(5000);
                    }
                    $('.form-result > .content', $this).html(data.message);
                    $('button[type="submit"]', $this).removeClass('clicked');
                    $this.trigger("reset");
                },
                error: function error() {
                    $('.form-result', $this).addClass('alert-danger').removeClass('alert-warning alert-success').css('display', 'block');
                    $('.form-result > .content', $this).html('Sorry, an error occurred.');
                    $('button[type="submit"]', $this).removeClass('clicked');
                }
            });
            return false;
        });

    }); 

    /*-------------------------------------
    Contact Form initiating
    -------------------------------------*/
	var contactForm = $('#contact-form');
	if (contactForm.length) {
		contactForm.validator().on('submit', function (e) {
			var $this = $(this),
				$target = contactForm.find('.form-response');
			if (e.isDefaultPrevented()) {
				$target.html("<div class='alert alert-success'><p>لطفاً تمام قسمت های مورد نیاز را انتخاب کنید.</p></div>");
			} else {
				$.ajax({
					url: "vendor/php/mailer.php",
					type: "POST",
					data: contactForm.serialize(),
					beforeSend: function () {
						$target.html("<div class='alert alert-info'><p>درحال بارگذاری ...</p></div>");
					},
					success: function (text) {
						if (text === "success") {
							$this[0].reset();
							$target.html("<div class='alert alert-success'><p>پیام با موفقیت ارسال شد.</p></div>");
						} else {
							$target.html("<div class='alert alert-success'><p>" + text + "</p></div>");
						}
					}
				});
				return false;
			}
		});
	}

    /*-------------------------------------
    Countdown activation code
    -------------------------------------*/
    $(function () {        
        var eventCounter = $(".countdown");
        if (eventCounter.length) {
            eventCounter.countdown("2024/2/12", function (e) {
                $(this).html(
                    e.strftime(
                        "<div class='countdown-section'><div><div class='countdown-number'>%D</div> <div class='countdown-unit'>روز</div> </div></div><div class='countdown-section'><div><div class='countdown-number'>%H</div> <div class='countdown-unit'>ساعت</div> </div></div><div class='countdown-section'><div><div class='countdown-number'>%M</div> <div class='countdown-unit'>دقیقه</div> </div></div><div class='countdown-section'><div><div class='countdown-number'>%S</div> <div class='countdown-unit'>ثانیه</div> </div></div>"
                    )
                );
            });
        }
    });

})(jQuery);