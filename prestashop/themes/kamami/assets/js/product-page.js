(function () {
	"use strict";

	function initProductImageGallery() {
		const $container = $(".js-images-container");
		if ($container.length === 0) {
			return;
		}

		$(document).on("click", ".js-thumb", function (e) {
			e.preventDefault();
			const $thumb = $(this);
			const $cover = $(".js-qv-product-cover");

			if ($cover.length === 0) {
				return;
			}

			const largeSrc =
				$thumb.data("image-large-src") || $thumb.attr("data-image-large-src");
			const mediumSrc =
				$thumb.data("image-medium-src") || $thumb.attr("data-image-medium-src");

			if (largeSrc) {
				$cover.attr("src", largeSrc);

				const alt = $thumb.attr("alt");
				const title = $thumb.attr("title");
				if (alt) $cover.attr("alt", alt);
				if (title) $cover.attr("title", title);
			}

			$(".js-thumb").removeClass("selected js-thumb-selected");
			$thumb.addClass("selected js-thumb-selected");
		});

		$(document).on("click", ".scroll-box-arrows .left", function (e) {
			e.preventDefault();
			const $mask = $(".js-qv-mask.mask.scroll");
			if ($mask.length) {
				$mask[0].scrollLeft -= 200;
			}
		});

		$(document).on("click", ".scroll-box-arrows .right", function (e) {
			e.preventDefault();
			const $mask = $(".js-qv-mask.mask.scroll");
			if ($mask.length) {
				$mask[0].scrollLeft += 200;
			}
		});
	}

	function initAddToCart() {
		const $form = $("#add-to-cart-or-refresh");
		const $button = $('.add-to-cart[data-button-action="add-to-cart"]');

		if ($button.length === 0) {
			return;
		}

		$form.on("submit", function (e) {
			const $btn = $(this).find(".add-to-cart");
			const $icon = $btn.find(".addcart_ico");

			$btn.addClass("loading").removeClass("no-added");
			$icon.find(".redfox-loading").show();
			$icon.find(".redfox-cart").hide();
			$icon.find(".redfox-checkmark").hide();
		});

		if (typeof prestashop !== "undefined") {
			prestashop.on("updateCart", function (event) {
				const $btn = $('.add-to-cart[data-button-action="add-to-cart"]');
				const $icon = $btn.find(".addcart_ico");

				$btn.removeClass("loading no-added").addClass("added");
				$icon.find(".redfox-loading").hide();
				$icon.find(".redfox-cart").hide();
				$icon.find(".redfox-checkmark").show();

				setTimeout(function () {
					$btn.removeClass("added").addClass("no-added");
					$icon.find(".redfox-checkmark").hide();
					$icon.find(".redfox-cart").show();
				}, 2000);
			});
		}
	}

	function showWishlistModal(message) {
		$(".fancybox-overlay, .fancybox-wrap").remove();

		const modalHtml = `
			<div class="fancybox-overlay fancybox-overlay-fixed" style="width: auto; height: auto; display: block;">
				<div class="fancybox-wrap fancybox-desktop fancybox-type-html fancybox-opened" tabindex="-1" style="width: 376px; height: auto; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); opacity: 1; overflow: visible;">
					<div class="fancybox-skin" style="padding: 0px; width: auto; height: auto;">
						<div class="fancybox-outer">
							<div class="fancybox-inner" style="overflow: auto; width: 376px; height: auto;">
								<p class="fancybox-error">${message}</p>
							</div>
						</div>
						<a title="Close" class="fancybox-item fancybox-close wishlist-modal-close" href="javascript:;"></a>
					</div>
				</div>
			</div>
		`;

		$("body").append(modalHtml);

		function closeModal() {
			$(".fancybox-overlay").fadeOut(200, function () {
				$(this).remove();
			});
		}

		$(".wishlist-modal-close, .fancybox-overlay").on("click", closeModal);

		$(document).on("keydown.wishlistModal", function (e) {
			if (e.keyCode === 27) {
				// ESC key
				closeModal();
				$(document).off("keydown.wishlistModal");
			}
		});
	}

	function initWishlist() {
		if (typeof window.WishlistCart === "undefined") {
			window.WishlistCart = function (
				listId,
				action,
				productId,
				combinationId,
				quantity,
			) {
				if (typeof blockwishlistController === "undefined") {
					showWishlistModal("Funkcjonalność listy życzeń niedostępna");
					return false;
				}

				$.ajax({
					url: blockwishlistController,
					method: "POST",
					dataType: "json",
					data: { action: "getAllWishList" },
					success: function (wishlistResponse) {
						const wishlists = wishlistResponse.wishlists || [];
						const defaultWishlist =
							wishlists.find((w) => w.default === 1 || w.default === "1") ||
							wishlists[0];

						if (!defaultWishlist) {
							showWishlistModal("Nie można znaleźć listy życzeń");
							return;
						}

						$.ajax({
							url: blockwishlistController,
							method: "POST",
							dataType: "json",
							data: {
								action: "addProductToWishList",
								params: {
									id_product: productId,
									id_product_attribute: combinationId || 0,
									quantity: quantity || 1,
									idWishList: defaultWishlist.id_wishlist,
								},
							},
							success: function (response) {
								if (response.success) {
									$("#wishlist_button").addClass("added");
									showWishlistModal("Produkt został dodany do listy życzeń");
									setTimeout(function () {
										$("#wishlist_button").removeClass("added");
									}, 2000);
								} else {
									const msg =
										response.message ||
										"Wystąpił błąd podczas dodawania do listy życzeń";
									if (
										msg.indexOf("zalogowany") !== -1 ||
										msg.indexOf("logged") !== -1
									) {
										showWishlistModal(
											"Musisz być zalogowany aby zarządzać listą życzeń",
										);
									} else {
										showWishlistModal(msg);
									}
								}
							},
							error: function () {
								showWishlistModal(
									"Wystąpił błąd podczas dodawania do listy życzeń",
								);
							},
						});
					},
					error: function () {
						showWishlistModal("Wystąpił błąd podczas pobierania listy życzeń");
					},
				});

				return false;
			};
		}
	}

	function init() {
		const isProductPage =
			$("body").hasClass("product-id") || $(".product-details").length > 0;

		if (!isProductPage) {
			return;
		}

		initProductImageGallery();
		initAddToCart();
		initWishlist();
	}

	$(document).ready(function () {
		init();
	});

	$(document).on("updatedProduct", function () {
		init();
	});
})();
