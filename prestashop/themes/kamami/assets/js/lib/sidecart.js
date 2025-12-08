/**
 * SideCart - Shopping cart sidebar component
 * Opens a side panel when clicking on the cart icon with slide-in animation
 *
 * @example
 * const sidecart = new SideCart();
 * sidecart.init();
 */
class SideCart {
	constructor(options = {}) {
		this.options = {
			cartSelector: ".cart_block_ajax",
			overlayClass: "cart-overlayer",
			openClass: "dfx-cart-open",
			desktopCartSelector: "#_desktop_cart",
			mobileCartSelector: "#_mobile_cart",
			closeButtonSelector: ".cartclosebtn",
			addToCartSelector: ".add-to-cart",
			removeFromCartSelector: ".remove-from-cart",
			blockCartSelector: ".blockcart",
			fadeSpeed: 500,
			...options,
		};
	}

	init() {
		this._setupDOM();
		this._bindOpenCart();
		this._bindCloseCart();
		this._bindAddToCart();
		this._bindRemoveFromCart();
	}

	_setupDOM() {
		$(this.options.cartSelector).insertAfter("main");

		if (!$(`.${this.options.overlayClass}`).length) {
			$(`<div class="${this.options.overlayClass}"></div>`).insertAfter("main");
		}

		$(`.${this.options.overlayClass}`).not(":first").remove();
		$(this.options.cartSelector).not(":first").remove();
	}

	_bindOpenCart() {
		const { desktopCartSelector, mobileCartSelector } = this.options;

		$(`${desktopCartSelector}, ${mobileCartSelector}`)
			.off("click.sidecart")
			.on("click.sidecart", (e) => {
				e.preventDefault();
				this.open();
			});
	}

	_bindCloseCart() {
		const { closeButtonSelector, overlayClass } = this.options;

		$(`${closeButtonSelector}, .${overlayClass}`)
			.off("click.sidecart")
			.on("click.sidecart", () => {
				this.close();
			});
	}

	_bindAddToCart() {
		$("body").on("click", this.options.addToCartSelector, function () {
			const productId = $(this).data("id-product");
			$(`.add-to-cart[data-id-product="${productId}"]`)
				.addClass("is-added disabled")
				.removeClass("no-added");
			$(this).addClass("is-added disabled").removeClass("no-added");
		});
	}

	_bindRemoveFromCart() {
		$("body").on("click", this.options.removeFromCartSelector, function (e) {
			const productId = $(this).data("id-product");
			$(`.add-to-cart[data-id-product="${productId}"]`)
				.addClass("no-added disabled")
				.removeClass("is-added");
			e.preventDefault();
		});
	}

	open() {
		$("html").addClass(this.options.openClass);
		$(`.${this.options.overlayClass}`).fadeIn(this.options.fadeSpeed);
	}

	close() {
		$("html").removeClass(this.options.openClass);
		$(`.${this.options.overlayClass}`).fadeOut(this.options.fadeSpeed);
	}

	refresh() {
		const refreshUrl = $(this.options.blockCartSelector).data("refresh-url");
		if (!refreshUrl) return;

		$.ajax({
			url: refreshUrl,
			type: "POST",
			dataType: "json",
			success: (resp) => this._handleRefreshSuccess(resp),
			error: (_, __, error) => console.error("Cart refresh error:", error),
		});
	}

	_handleRefreshSuccess(resp) {
		if (resp.cart) {
			$(".cart-products-count").text(resp.cart.products_count);
			$(".ajax_cart_total").text(resp.cart.subtotals.products.value);

			if (resp.cart.products_count > 0) {
				$(this.options.blockCartSelector)
					.removeClass("inactive")
					.addClass("active");
			} else {
				$(this.options.blockCartSelector)
					.removeClass("active")
					.addClass("inactive");
			}
		}

		$.get(window.location.href, (html) => {
			const $newSidebar = $(html).find(this.options.cartSelector);
			if ($newSidebar.length) {
				$(this.options.cartSelector).replaceWith($newSidebar);
				this.init();
			}
		});
	}
}
