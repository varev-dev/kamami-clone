$(document).ready(function () {
	initProductSorting();
	initItemsPerPage();
});

function initProductSorting() {
	$(document).on("click", ".products-sort-order .select-title", function (e) {
		e.preventDefault();
		e.stopPropagation();

		const $dropdown = $(this).closest(".products-sort-order");
		const $menu = $dropdown.find(".dropdown-menu");
		const isOpen = $dropdown.hasClass("open");

		$(".products-sort-order.open")
			.not($dropdown)
			.removeClass("open")
			.find(".dropdown-menu")
			.hide();

		if (isOpen) {
			$dropdown.removeClass("open");
			$menu.hide();
		} else {
			$dropdown.addClass("open");
			$menu.show();
		}
	});

	$(document).on(
		"click",
		".products-sort-order .select-list, .products-sort-order .js-search-link",
		function (e) {
			e.preventDefault();

			const sortUrl = $(this).attr("href");
			if (sortUrl) {
				window.location.href = sortUrl;
			}
		},
	);

	$(document).on("click", function (e) {
		if (!$(e.target).closest(".products-sort-order").length) {
			$(".products-sort-order")
				.removeClass("open")
				.find(".dropdown-menu")
				.hide();
		}
	});
}

function initItemsPerPage() {
	$(document).on("click", ".ppiselval", function (e) {
		e.preventDefault();
		e.stopPropagation();

		const itemsPerPage = parseInt($(this).text().trim());

		// Update URL with resultsPerPage parameter (PrestaShop uses this)
		const currentUrl = new URL(window.location.href);
		currentUrl.searchParams.set("resultsPerPage", itemsPerPage);
		currentUrl.searchParams.set("page", "1");

		window.location.href = currentUrl.toString();
	});
}
