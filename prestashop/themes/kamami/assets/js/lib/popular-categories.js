/**
 * Popular Categories - Owl Carousel initialization
 * Creates a responsive carousel for the popular categories section on homepage
 */

(function () {
	"use strict";

	/**
	 * Initialize popular categories carousel with Owl Carousel
	 */
	function initPopularCategories() {
		const $carousel = $(".top_catlink");

		if (!$carousel.length) {
			return;
		}

		// Check if Owl Carousel is available
		if (typeof $.fn.owlCarousel === "undefined") {
			console.warn("Owl Carousel is not loaded");
			return;
		}

		// Don't initialize if already initialized
		if ($carousel.hasClass("owl-loaded")) {
			return;
		}

		// Initialize Owl Carousel with responsive configuration
		$carousel.owlCarousel({
			loop: false,
			nav: true,
			dots: false,
			responsiveBaseElement: "#content-wrapper",
			items: 6,
			navText: [
				'<span aria-label="Previous">‹</span>',
				'<span aria-label="Next">›</span>',
			],
			responsive: {
				0: {
					items: 1,
					margin: 10,
				},
				320: {
					items: 2,
					slideBy: 1,
					margin: 10,
				},
				420: {
					items: 3,
					slideBy: 1,
					margin: 10,
				},
				682: {
					items: 4,
					slideBy: 1,
					margin: 10,
				},
				768: {
					items: 5,
					slideBy: 1,
					margin: 10,
				},
				992: {
					items: 5,
					slideBy: 1,
					margin: 15,
				},
				1200: {
					items: 6,
					slideBy: 1,
					margin: 15,
				},
			},
		});
	}

	// Initialize when DOM is ready
	if (typeof jQuery !== "undefined") {
		$(document).ready(function () {
			initPopularCategories();
		});
	} else {
		// Wait for jQuery if not available yet
		window.addEventListener("DOMContentLoaded", function () {
			if (typeof jQuery !== "undefined") {
				initPopularCategories();
			}
		});
	}
})();

