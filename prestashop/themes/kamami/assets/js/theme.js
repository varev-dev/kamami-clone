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

	// Initialize side cart
	const sidecart = new SideCart();
	sidecart.init();

	// Listen f or PrestaShop cart updates
	if (typeof prestashop !== "undefined") {
		prestashop.on("updateCart", function (event) {
			sidecart.refresh();

			if (event && event.reason && event.reason.linkAction === "add-to-cart") {
				sidecart.open();
			}
		});
	}
});
