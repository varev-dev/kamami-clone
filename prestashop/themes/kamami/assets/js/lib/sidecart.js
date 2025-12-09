/**
 * SideCart - Simple shopping cart sidebar
 */
const SideCart = {
	cartSelector: ".cart_block_ajax",
	overlaySelector: ".cart-overlayer",

	init() {
		// Open cart on icon click
		$(document).on("click", "#_desktop_cart, #_mobile_cart", (e) => {
			e.preventDefault();
			this.open();
		});

		// Close cart
		$(document).on("click", ".cartclosebtn, .cart-overlayer", () =>
			this.close(),
		);

		// Remove item from cart
		$(document).on("click", ".remove-from-cart", (e) => {
			e.preventDefault();
			const $link = $(e.currentTarget);
			const url = $link.attr("href");
			if (!url) return;

			$.get(url + (url.includes("?") ? "&" : "?") + "ajax=1", (resp) => {
				prestashop.emit("updateCart", {
					reason: {
						idProduct: $link.data("id-product"),
						idProductAttribute: $link.data("id-product-attribute") || 0,
						linkAction: "delete-from-cart",
					},
					resp,
				});
			});
		});

		// Refresh cart content on PrestaShop cart update
		prestashop.on("updateCart", (event) => {
			this.refresh();
			// Only auto-open when adding, not when deleting
			if (event?.reason?.linkAction !== "delete-from-cart") {
				this.open();
			}
		});
	},

	open() {
		$("html").addClass("dfx-cart-open");
		$(this.overlaySelector).fadeIn(300);
	},

	close() {
		$("html").removeClass("dfx-cart-open");
		$(this.overlaySelector).fadeOut(300);
	},

	refresh() {
		const refreshUrl = $(".blockcart").data("refresh-url");
		if (!refreshUrl) return;

		$.post(refreshUrl, (resp) => {
			if (resp.preview) {
				const $preview = $(resp.preview);
				// Use filter() to get only the cart element (preview may have multiple root elements)
				let $newCart = $preview.filter(this.cartSelector);
				if (!$newCart.length) {
					$newCart = $preview.find(this.cartSelector);
				}
				if ($newCart.length) {
					$(this.cartSelector).replaceWith($newCart);
				}
			}
			if (resp.cart) {
				$(".cart-products-count").text(resp.cart.products_count);
			}
		});
	},
};
