/**
 * Brand Carousel - Owl Carousel initialization for manufacturer carousel
 * Handles revealOnScroll animation and carousel initialization
 */

(function () {
	"use strict";

	/**
	 * Initialize brand carousel with reveal on scroll
	 */
	function initBrandCarousel() {
		const $carousel = $(".manufacturer-carousel");

		if (!$carousel.length) {
			return;
		}

		// Check if Owl Carousel is available
		if (typeof $.fn.owlCarousel === "undefined") {
			console.warn("Owl Carousel is not loaded");
			return;
		}

		// Initialize reveal on scroll
		function revealOnScroll() {
			$carousel.each(function () {
				const $el = $(this);
				const animation = $el.data("animation") || "fadeInUp";
				const timeout = parseInt($el.data("timeout")) || 0;

				if ($el.hasClass("animated")) {
					return;
				}

				const elementTop = $el.offset().top;
				const elementBottom = elementTop + $el.outerHeight();
				const viewportTop = $(window).scrollTop();
				const viewportBottom = viewportTop + $(window).height();

				if (elementBottom > viewportTop && elementTop < viewportBottom) {
					setTimeout(function () {
						$el.addClass("animated " + animation);
					}, timeout);
				}
			});
		}

		// Initialize each carousel individually
		$carousel.each(function () {
			const $el = $(this);

			// Don't initialize if already initialized
			if ($el.hasClass("owl-loaded")) {
				return;
			}

			// Initialize Owl Carousel
			$el.owlCarousel({
				items: 5,
				loop: true, // Enable loop for autoplay to work smoothly
				margin: 10,
				nav: true,
				dots: false,
				autoplay: true,
				autoplayTimeout: 5000, // 5 seconds
				autoplayHoverPause: true, // Pause on hover
				navText: ["‹", "›"],
				responsive: {
					0: {
						items: 2,
					},
					480: {
						items: 3,
					},
					768: {
						items: 4,
					},
					992: {
						items: 5,
					},
					1200: {
						items: 6,
					},
				},
				onInitialized: function () {
					// Trigger reveal animation after carousel is initialized
					revealOnScroll();
				},
			});
		});

		// Check on scroll for reveal animation
		$(window).on("scroll", revealOnScroll);

		// Initial check
		revealOnScroll();
	}

	// Initialize when DOM is ready
	if (typeof jQuery !== "undefined") {
		$(document).ready(function () {
			initBrandCarousel();
		});
	} else {
		// Wait for jQuery if not available yet
		window.addEventListener("DOMContentLoaded", function () {
			if (typeof jQuery !== "undefined") {
				initBrandCarousel();
			}
		});
	}
})();
