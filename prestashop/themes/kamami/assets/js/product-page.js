(function () {
	"use strict";

	function initProductImageGallery() {
		const $container = $(".js-images-container");
		if ($container.length === 0) {
			return;
		}

		const $zoomContainer = $("#productZoom");
		if ($zoomContainer.length) {
			$zoomContainer.zoom();

			$(document).on("click", ".js-thumb", function (e) {
				e.preventDefault();
				const $thumb = $(this);
				const $cover = $(".js-qv-product-cover");
				const largeSrc = $thumb.attr("data-image-large-src");

				if ($cover.length && largeSrc) {
					$cover.attr("src", largeSrc);
					const alt = $thumb.attr("alt");
					const title = $thumb.attr("title");
					if (alt) $cover.attr("alt", alt);
					if (title) $cover.attr("title", title);
					$zoomContainer.trigger("zoom.destroy").zoom({ url: largeSrc });
				}

				$(".js-thumb").removeClass("selected js-thumb-selected");
				$thumb.addClass("selected js-thumb-selected");
			});
		}

		$(document).on(
			"click",
			".layer[data-toggle='modal'][data-target='#product-modal']",
			function (e) {
				e.preventDefault();
				e.stopPropagation();
				const $modal = $("#product-modal");
				if ($modal.length === 0) {
					return;
				}

				$(".modal-backdrop").remove();
				$modal.css("display", "block").addClass("in");
				$("body").addClass("modal-open");
				const $backdrop = $(
					'<div class="modal-backdrop fade in" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 1040; background-color: rgba(0,0,0,0.5);"></div>',
				);
				$("body").append($backdrop);

				function closeModal() {
					$modal.css("display", "none").removeClass("in");
					$("body").removeClass("modal-open");
					$backdrop.fadeOut(200, function () {
						$(this).remove();
					});
					$(document).off("keydown.productModal");
				}

				$(document).on("keydown.productModal", function (keyEvent) {
					if (keyEvent.keyCode === 27) {
						closeModal();
					}
				});

				$backdrop.on("click", closeModal);

				$modal.on("click", function (clickEvent) {
					if (
						$(clickEvent.target).is($modal) ||
						$(clickEvent.target).hasClass("modal-backdrop")
					) {
						closeModal();
					}
				});

				$modal.find("[data-dismiss='modal'], .close").on("click", closeModal);
			},
		);

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
		initWishlist();
		initMagnifier();
		initProductAccessories();
	}

	function initMagnifier() {
		$(document).on("click", "#product-modal .js-modal-thumb", function (e) {
			e.preventDefault();
			const $thumb = $(this);
			const largeSrc = $thumb.attr("data-image-large-src");
			if (largeSrc) {
				$("#product-modal .js-modal-product-cover").attr("src", largeSrc);
			}
			$("#product-modal .js-modal-thumb").removeClass("selected");
			$thumb.addClass("selected");
		});

		$(document).on("click", "#product-modal .js-modal-arrow-up", function (e) {
			e.preventDefault();
			const $mask = $("#product-modal .js-modal-mask");
			if ($mask.length) {
				$mask[0].scrollTop -= 100;
			}
		});

		$(document).on(
			"click",
			"#product-modal .js-modal-arrow-down",
			function (e) {
				e.preventDefault();
				const $mask = $("#product-modal .js-modal-mask");
				if ($mask.length) {
					$mask[0].scrollTop += 100;
				}
			},
		);
	}

	function initProductAccessories() {
		const $carousel = $("#product-accessories.product-carousel");
		if (
			!$carousel.length ||
			typeof $.fn.owlCarousel === "undefined" ||
			$carousel.hasClass("owl-loaded")
		) {
			return;
		}

		function setEqualHeights() {
			const $items = $carousel.find(".owl-item.active .product-miniature");
			if (!$items.length) return;
			let maxHeight = 0;
			$items.css("height", "auto").each(function () {
				maxHeight = Math.max(maxHeight, $(this).outerHeight());
			});
			$items.css("height", maxHeight + "px");
		}

		$carousel.owlCarousel({
			loop: false,
			nav: true,
			dots: false,
			margin: 0,
			items: 5,
			navText: ["‹", "›"],
			onInitialized: setEqualHeights,
			onResized: setEqualHeights,
		});
	}

	$(document).ready(init);

	$(document).on("updatedProduct", function () {
		init();
	});
})();
