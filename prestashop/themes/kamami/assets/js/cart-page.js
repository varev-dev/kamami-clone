function initCartQuantityButtons() {
	let activeUpdateRequest = null;
	let activeRefreshRequest = null;

	function refreshCartSections() {
		const $cartOverview = $(".js-cart");
		if (!$cartOverview.length) return;

		const refreshUrl = $cartOverview.data("refresh-url");
		if (!refreshUrl) return;

		if (activeRefreshRequest) {
			activeRefreshRequest.abort();
		}

		activeRefreshRequest = $.ajax({
			url: refreshUrl,
			type: "POST",
			dataType: "json",
			success: function (resp) {
				if (!resp) return;

				if (resp.cart_detailed) {
					const $newCart = $(resp.cart_detailed);
					if ($newCart.find(".js-cart").length) {
						$cartOverview.html($newCart.find(".js-cart").html());
					} else {
						$cartOverview.html($newCart.html());
					}
				}

				if (resp.cart_detailed_totals) {
					const $totals = $(".js-cart-detailed-totals");
					if ($totals.length) {
						$totals.html($(resp.cart_detailed_totals).html());
					}
				}

				if (resp.cart_summary_totals) {
					const $summaryTotals = $(".js-cart-summary-totals");
					if ($summaryTotals.length) {
						$summaryTotals.html($(resp.cart_summary_totals).html());
					}
				}

				if (resp.cart_detailed_subtotals) {
					const $subtotals = $(".js-cart-detailed-subtotals");
					if ($subtotals.length) {
						$subtotals.html($(resp.cart_detailed_subtotals).html());
					}
				}

				if (resp.cart_summary_products) {
					const $summaryProducts = $(".js-cart-summary-products");
					if ($summaryProducts.length) {
						$summaryProducts.html($(resp.cart_summary_products).html());
					}
				}

				if (resp.cart_summary_items_subtotal) {
					const $itemsSubtotal = $(".js-cart-summary-items-subtotal");
					if ($itemsSubtotal.length) {
						$itemsSubtotal.html($(resp.cart_summary_items_subtotal).html());
					}
				}

				if (resp.cart_summary_subtotals_container) {
					const $subtotalsContainer = $(".js-cart-summary-subtotals");
					if ($subtotalsContainer.length) {
						$subtotalsContainer.html(
							$(resp.cart_summary_subtotals_container).html(),
						);
					}
				}

				if (resp.cart_detailed_actions) {
					const $actions = $(".js-cart-detailed-actions");
					if ($actions.length) {
						$actions.html($(resp.cart_detailed_actions).html());
					}
				}

				if (resp.cart_voucher) {
					const $voucher = $(".js-cart-voucher");
					if ($voucher.length) {
						$voucher.closest(".block-promo").html($(resp.cart_voucher).html());
					}
				}

				if (resp.cart_summary_top) {
					const $summaryTop = $(".js-cart-summary-top");
					if ($summaryTop.length) {
						$summaryTop.html($(resp.cart_summary_top).html());
					}
				}

				prestashop.emit("updateCart", {
					reason: {
						linkAction: "update-quantity",
					},
					resp: resp,
				});
			},
			error: function () {},
			complete: function () {
				activeRefreshRequest = null;
			},
		});
	}

	function updateQuantity(url) {
		if (activeUpdateRequest) {
			activeUpdateRequest.abort();
		}

		activeUpdateRequest = $.ajax({
			url: url + (url.includes("?") ? "&" : "?") + "ajax=1",
			type: "POST",
			dataType: "text",
			success: function (resp) {
				let parsedResp = { success: true };

				if (resp && resp.trim()) {
					try {
						parsedResp = JSON.parse(resp);
					} catch {
						parsedResp = { success: true };
					}
				}

				if (parsedResp && (parsedResp.success || !parsedResp.hasError)) {
					refreshCartSections();
				} else if (parsedResp && parsedResp.hasError && parsedResp.errors) {
					alert(parsedResp.errors.join("\n"));
				} else {
					refreshCartSections();
				}
			},
			error: function () {
				refreshCartSections();
			},
			complete: function () {
				activeUpdateRequest = null;
			},
		});
	}

	$(document).on("click", ".js-increase-product-quantity", function (e) {
		e.preventDefault();
		const $input = $(this)
			.closest(".bootstrap-touchspin")
			.find(".js-cart-line-product-quantity");
		const upUrl = $input.data("up-url");
		if (upUrl) updateQuantity(upUrl);
	});

	$(document).on("click", ".js-decrease-product-quantity", function (e) {
		e.preventDefault();
		const $input = $(this)
			.closest(".bootstrap-touchspin")
			.find(".js-cart-line-product-quantity");
		const downUrl = $input.data("down-url");
		if (downUrl) updateQuantity(downUrl);
	});

	$(document).on("focus", ".js-cart-line-product-quantity", function () {
		const $input = $(this);
		$input.data("initial-quantity", parseInt($input.val()) || 1);
	});

	$(document).on("blur", ".js-cart-line-product-quantity", function () {
		const $input = $(this);
		const updateUrl = $input.data("update-url");
		const initialQuantity = $input.data("initial-quantity") || 1;
		let newQuantity = parseInt($input.val()) || 1;

		if (newQuantity <= 0) {
			newQuantity = 1;
			$input.val(1);
		}

		if (updateUrl && newQuantity !== initialQuantity) {
			const diff = newQuantity - initialQuantity;
			const op = diff > 0 ? "up" : "down";
			const qty = Math.abs(diff);
			const separator = updateUrl.includes("?") ? "&" : "?";
			const url = updateUrl + separator + "qty=" + qty + "&op=" + op + "&ajax=1";
			updateQuantity(url);
		}
	});
}

$(document).ready(function () {
	initCartQuantityButtons();
});
