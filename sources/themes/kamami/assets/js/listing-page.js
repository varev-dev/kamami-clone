$(document).ready(function () {
	initProductSorting();
	initItemsPerPage();
	initProductViewToggle();
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

function initProductViewToggle() {
	// Get saved view preference or default to grid
	const currentView = localStorage.getItem("productListView") || "grid";

	// Apply saved view on page load
	if (currentView === "list") {
		$("#js-product-list").removeClass("active_grid").addClass("active_list");
		$("#grid").removeClass("selected_grid");
		$("#list").addClass("selected_list");
	} else {
		$("#js-product-list").removeClass("active_list").addClass("active_grid");
		$("#list").removeClass("selected_list");
		$("#grid").addClass("selected_grid");
	}

	// Handle grid view click
	$(document).on("click", "#grid a", function (e) {
		e.preventDefault();

		$("#js-product-list").removeClass("active_list").addClass("active_grid");
		$("#list").removeClass("selected_list");
		$("#grid").addClass("selected_grid");

		localStorage.setItem("productListView", "grid");
	});

	// Handle list view click
	$(document).on("click", "#list a", function (e) {
		e.preventDefault();

		$("#js-product-list").removeClass("active_grid").addClass("active_list");
		$("#grid").removeClass("selected_grid");
		$("#list").addClass("selected_list");

		localStorage.setItem("productListView", "list");
	});
}
