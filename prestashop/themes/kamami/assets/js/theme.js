/**
 * Theme initialization
 */
$(document).ready(function () {
	// Initialize dropdowns
	const $dropdowns = $(".js-dropdown");
	if ($dropdowns.length) {
		const dropdown = new DropDown($dropdowns);
		dropdown.init();
	}

	SideCart.init();
});

$(document).ready(function () {
	// Initialize category tree collapse functionality
	initCategoryTreeCollapse();

	// Initialize quickview functionality
	initQuickView();

	// Fix lazy loading for product thumbnails - ensure images load even if lazy load script fails
	initLazyLoadFallback();
});

/**
 * Initialize lazy load fallback for product thumbnails
 * Ensures images load even if the lazy loading script doesn't work
 */
function initLazyLoadFallback() {
	// Check for images with data-src that haven't loaded after a short delay
	setTimeout(function () {
		$(".js-lazyload[data-src]").each(function () {
			const $img = $(this);
			// If image hasn't loaded (still showing placeholder or has no natural width)
			if (
				!$img.attr("src") ||
				$img.attr("src").indexOf("data:image/svg+xml") !== -1
			) {
				const dataSrc = $img.attr("data-src");
				if (dataSrc) {
					$img.attr("src", dataSrc).removeAttr("data-src");
				}
			}
		});
	}, 500);

	// Also handle images that come into viewport
	if (typeof IntersectionObserver !== "undefined") {
		const imageObserver = new IntersectionObserver(
			function (entries, observer) {
				entries.forEach(function (entry) {
					if (entry.isIntersecting) {
						const $img = $(entry.target);
						const dataSrc = $img.attr("data-src");
						if (
							dataSrc &&
							(!$img.attr("src") ||
								$img.attr("src").indexOf("data:image/svg+xml") !== -1)
						) {
							$img.attr("src", dataSrc).removeAttr("data-src");
							observer.unobserve(entry.target);
						}
					}
				});
			},
		);

		$(".js-lazyload[data-src]").each(function () {
			imageObserver.observe(this);
		});
	}
}

/**
 * Initialize quickview modal functionality
 * Handles clicks on quick-view links and loads product data via AJAX
 */
function initQuickView() {
	// Touchspin quantity buttons (delegated for dynamic modals)
	$(document).on("click", ".bootstrap-touchspin-up", function () {
		const $input = $(this).closest(".bootstrap-touchspin").find("input");
		$input.val(parseInt($input.val() || 1) + 1);
	});

	$(document).on("click", ".bootstrap-touchspin-down", function () {
		const $input = $(this).closest(".bootstrap-touchspin").find("input");
		const val = parseInt($input.val() || 1);
		if (val > 1) $input.val(val - 1);
	});

	// Close quickview modal when cart is updated
	prestashop.on("updateCart", function () {
		$(".quickview").css("display", "none").removeClass("in").remove();
		$("#quickview-backdrop").remove();
	});

	$(document).on(
		"click",
		'a.quick-view[data-link-action="quickview"]',
		function (e) {
			e.preventDefault();

			const $link = $(this);
			const $productMiniature = $link.closest(
				".js-product-miniature, .product-miniature",
			);
			const productId =
				$productMiniature.data("id-product") ||
				$productMiniature.data("idProduct");
			const productAttributeId =
				$productMiniature.data("id-product-attribute") ||
				$productMiniature.data("idProductAttribute") ||
				0;

			if (!productId) return;

			// Build quickview URL
			const $productLink = $productMiniature
				.find("a.thumbnail, a.name")
				.first();
			const productUrl = $productLink.attr("href");
			let quickviewUrl;

			if (productUrl) {
				const separator = productUrl.indexOf("?") !== -1 ? "&" : "?";
				quickviewUrl = productUrl + separator + "action=quickview&ajax=1";
			} else {
				const baseUrl =
					typeof prestashop !== "undefined" &&
					prestashop.urls &&
					prestashop.urls.base_url
						? prestashop.urls.base_url
						: window.location.protocol + "//" + window.location.host;
				quickviewUrl =
					baseUrl +
					"/index.php?controller=product&id_product=" +
					productId +
					"&id_product_attribute=" +
					productAttributeId +
					"&action=quickview&ajax=1";
			}

			const modalId = "quickview-modal-" + productId + "-" + productAttributeId;
			$("#" + modalId).remove();
			$link.addClass("loading");

			$.ajax({
				url: quickviewUrl,
				type: "GET",
				dataType: "json",
				success: function (data) {
					if (!data || !data.quickview_html) {
						alert("Error: Invalid response from server.");
						return;
					}

					$("body").append(data.quickview_html);
					const $modal = $("#" + modalId);

					if ($modal.length === 0) return;

					// Show modal
					$modal
						.css("display", "block")
						.addClass("in")
						.attr("aria-hidden", "false");
					if ($("#quickview-backdrop").length === 0) {
						$("body").append(
							'<div class="modal-backdrop fade in" id="quickview-backdrop"></div>',
						);
					}

					const closeModal = function () {
						$modal
							.css("display", "none")
							.removeClass("in")
							.attr("aria-hidden", "true");
						$("#quickview-backdrop").remove();
						$modal.remove();
						$(document).off("keydown.quickview");
					};

					$modal.find(".close, [data-dismiss='modal']").on("click", closeModal);
					$("#quickview-backdrop").on("click", closeModal);
					$(document).on("keydown.quickview", function (e) {
						if (e.keyCode === 27) closeModal();
					});

					// Handle thumbnail clicks
					$modal.on("click", ".js-thumb", function () {
						const $thumb = $(this);
						const largeSrc =
							$thumb.data("image-large-src") || $thumb.data("imageLargeSrc");
						if (largeSrc) {
							$modal.find(".js-qv-product-cover").attr("src", largeSrc);
						}
						$modal.find(".js-thumb").removeClass("selected js-thumb-selected");
						$thumb.addClass("selected js-thumb-selected");
					});
				},
				error: function () {
					alert("Error loading product details.");
				},
				complete: function () {
					$link.removeClass("loading");
				},
			});
		},
	);
}

/**
 * Initialize category tree collapse functionality
 * Handles Bootstrap collapse events and updates aria-expanded attribute
 */
function initCategoryTreeCollapse() {
	const $categoryTree = $(".block-categories");

	if (!$categoryTree.length) {
		return;
	}

	// Handle Bootstrap collapse events
	$categoryTree.on("show.bs.collapse", ".collapse", function () {
		const $collapse = $(this);
		const collapseId = $collapse.attr("id");
		const $toggle = $categoryTree.find('[data-target="#' + collapseId + '"]');

		if ($toggle.length) {
			$toggle.attr("aria-expanded", "true");
		}
	});

	$categoryTree.on("hide.bs.collapse", ".collapse", function () {
		const $collapse = $(this);
		const collapseId = $collapse.attr("id");
		const $toggle = $categoryTree.find('[data-target="#' + collapseId + '"]');

		if ($toggle.length) {
			$toggle.attr("aria-expanded", "false");
		}
	});

	// Initialize collapse state on page load
	$categoryTree.find(".collapse").each(function () {
		const $collapse = $(this);
		const collapseId = $collapse.attr("id");
		const $toggle = $categoryTree.find('[data-target="#' + collapseId + '"]');

		if ($toggle.length) {
			// Check if collapse is shown (has 'show' or 'in' class, or is visible)
			const isExpanded =
				$collapse.hasClass("show") ||
				$collapse.hasClass("in") ||
				$collapse.is(":visible");
			$toggle.attr("aria-expanded", isExpanded ? "true" : "false");
		}
	});

	// Fallback: Manual toggle if Bootstrap collapse isn't working
	$categoryTree.on("click", ".collapse-icons", function (e) {
		e.preventDefault();
		const $toggle = $(this);
		const target = $toggle.attr("data-target");

		if (!target) {
			return;
		}

		const $target = $(target);

		if (!$target.length) {
			return;
		}

		// Try Bootstrap collapse first
		if (typeof $.fn.collapse !== "undefined") {
			$target.collapse("toggle");
		} else {
			// Fallback: manual toggle
			const isExpanded = $toggle.attr("aria-expanded") === "true";

			if (isExpanded) {
				$target.slideUp(300);
				$toggle.attr("aria-expanded", "false");
			} else {
				$target.slideDown(300);
				$toggle.attr("aria-expanded", "true");
			}
		}
	});
}
