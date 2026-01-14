/**
 * Home Slider - Owl Carousel initialization for homepage image slider
 * Creates a responsive slider with autoplay, lazy loading, and progress bar
 */

(function () {
	"use strict";

	// Slider configuration
	const SLIDER_CONFIG = {
		autoplayTimeout: 8000, // 8 seconds per slide
		transitionSpeed: 250, // Animation speed in ms
	};

	/**
	 * Initialize home slider with Owl Carousel
	 */
	function initHomeSlider() {
		const $slider = $("#dfx-slider");
		const $wrapper = $slider.closest(".simple-slider");
		const $progress = $wrapper.find(".slide-progress");

		if (!$slider.length) {
			return;
		}

		// Check if Owl Carousel is available
		if (typeof $.fn.owlCarousel === "undefined") {
			console.warn("Owl Carousel is not loaded");
			return;
		}

		// Don't initialize if already initialized
		if ($slider.hasClass("owl-loaded")) {
			return;
		}

		// Initialize Owl Carousel
		$slider.owlCarousel({
			items: 1,
			loop: true,
			margin: 0,
			nav: true,
			dots: true,
			autoplay: true,
			autoplayTimeout: SLIDER_CONFIG.autoplayTimeout,
			autoplayHoverPause: true,
			smartSpeed: SLIDER_CONFIG.transitionSpeed,
			lazyLoad: true,
			navText: [
				'<span aria-label="Previous">‹</span>',
				'<span aria-label="Next">›</span>',
			],
			responsive: {
				0: {
					nav: false,
					dots: true,
				},
				768: {
					nav: true,
					dots: true,
				},
			},
			onInitialized: function () {
				// Mark slider as initialized
				$wrapper.addClass("initialized");
				// Start progress bar
				startProgress();
			},
			onTranslate: function () {
				// Reset progress bar on slide change
				resetProgress();
			},
			onTranslated: function () {
				// Restart progress bar after transition
				startProgress();
			},
		});

		/**
		 * Start the progress bar animation
		 */
		function startProgress() {
			if (!$progress.length) return;

			$progress.css({
				width: "0%",
				transition: "none",
			});

			// Force reflow
			$progress[0].offsetHeight;

			$progress.css({
				width: "100%",
				transition: "width " + SLIDER_CONFIG.autoplayTimeout + "ms linear",
			});
		}

		/**
		 * Reset progress bar
		 */
		function resetProgress() {
			if (!$progress.length) return;

			$progress.css({
				width: "0%",
				transition: "none",
			});
		}

		// Pause progress on hover
		$slider.on("mouseenter", function () {
			$progress.css("animation-play-state", "paused");
		});

		$slider.on("mouseleave", function () {
			$progress.css("animation-play-state", "running");
		});
	}

	// Initialize when DOM is ready
	if (typeof jQuery !== "undefined") {
		$(document).ready(function () {
			initHomeSlider();
		});
	} else {
		// Wait for jQuery if not available yet
		window.addEventListener("DOMContentLoaded", function () {
			if (typeof jQuery !== "undefined") {
				initHomeSlider();
			}
		});
	}
})();

