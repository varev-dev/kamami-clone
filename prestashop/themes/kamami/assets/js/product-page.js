/**
 * Kamami theme - Product page JavaScript
 * Handles product page interactions: image gallery, quantity selector, add to cart, etc.
 */

(function () {
	"use strict";

	/**
	 * Product Image Gallery
	 * Handles thumbnail navigation and scrolling
	 */
	function initProductImageGallery() {
		const $container = $(".js-images-container");
		if ($container.length === 0) return;

		// Thumbnail click handler
		$(document).on("click", ".js-thumb", function (e) {
			e.preventDefault();
			const $thumb = $(this);
			const $cover = $(".js-qv-product-cover");

			if ($cover.length === 0) return;

			// Get image sources from data attributes
			const largeSrc =
				$thumb.data("image-large-src") || $thumb.attr("data-image-large-src");
			const mediumSrc =
				$thumb.data("image-medium-src") || $thumb.attr("data-image-medium-src");

			if (largeSrc) {
				// Update main product image
				$cover.attr("src", largeSrc);

				// Update alt and title if available
				const alt = $thumb.attr("alt");
				const title = $thumb.attr("title");
				if (alt) $cover.attr("alt", alt);
				if (title) $cover.attr("title", title);
			}

			// Update selected state
			$(".js-thumb").removeClass("selected js-thumb-selected");
			$thumb.addClass("selected js-thumb-selected");
		});

		// Scroll box arrows
		$(document).on("click", ".scroll-box-arrows .left", function (e) {
			e.preventDefault();
			$(".js-qv-mask.mask.scroll")[0].scrollLeft -= 200;
		});

		$(document).on("click", ".scroll-box-arrows .right", function (e) {
			e.preventDefault();
			$(".js-qv-mask.mask.scroll")[0].scrollLeft += 200;
		});
	}

	/**
	 * Add to Cart Button
	 * Handles button states and visual feedback
	 */
	function initAddToCart() {
		const $form = $("#add-to-cart-or-refresh");
		const $button = $('.add-to-cart[data-button-action="add-to-cart"]');

		if ($button.length === 0) return;

		// Handle form submission
		$form.on("submit", function (e) {
			const $btn = $(this).find(".add-to-cart");
			const $icon = $btn.find(".addcart_ico");

			// Show loading state
			$btn.addClass("loading").removeClass("no-added");
			$icon.find(".redfox-loading").show();
			$icon.find(".redfox-cart").hide();
			$icon.find(".redfox-checkmark").hide();
		});

		// Listen for cart update events (from PrestaShop core)
		if (typeof prestashop !== "undefined") {
			prestashop.on("updateCart", function (event) {
				const $btn = $('.add-to-cart[data-button-action="add-to-cart"]');
				const $icon = $btn.find(".addcart_ico");

				// Show success state
				$btn.removeClass("loading no-added").addClass("added");
				$icon.find(".redfox-loading").hide();
				$icon.find(".redfox-cart").hide();
				$icon.find(".redfox-checkmark").show();

				// Reset after delay
				setTimeout(function () {
					$btn.removeClass("added").addClass("no-added");
					$icon.find(".redfox-checkmark").hide();
					$icon.find(".redfox-cart").show();
				}, 2000);
			});
		}
	}

	/**
	 * Initialize all product page functionality
	 */
	function init() {
		// Only run on product pages
		if (!$("body").hasClass("product-id") && !$(".product-details").length) {
			return;
		}

		initProductImageGallery();
		initAddToCart();
	}

	// Initialize when DOM is ready
	$(document).ready(function () {
		init();
	});

	// Re-initialize after AJAX updates (for variant changes, etc.)
	$(document).on("updatedProduct", function () {
		init();
	});
})();
