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

	// Listen for PrestaShop cart updates
	if (typeof prestashop !== "undefined") {
		prestashop.on("updateCart", function (event) {
			sidecart.refresh();

			if (event && event.reason && event.reason.linkAction === "add-to-cart") {
				sidecart.open();
			}
		});
	}

	// Initialize category tree collapse functionality
	initCategoryTreeCollapse();
});

/**
 * Initialize category tree collapse functionality
 * Handles Bootstrap collapse events and updates aria-expanded attribute
 */
function initCategoryTreeCollapse() {
	const $categoryTree = $('.block-categories');
	
	if (!$categoryTree.length) {
		return;
	}

	// Handle Bootstrap collapse events
	$categoryTree.on('show.bs.collapse', '.collapse', function() {
		const $collapse = $(this);
		const collapseId = $collapse.attr('id');
		const $toggle = $categoryTree.find('[data-target="#' + collapseId + '"]');
		
		if ($toggle.length) {
			$toggle.attr('aria-expanded', 'true');
		}
	});

	$categoryTree.on('hide.bs.collapse', '.collapse', function() {
		const $collapse = $(this);
		const collapseId = $collapse.attr('id');
		const $toggle = $categoryTree.find('[data-target="#' + collapseId + '"]');
		
		if ($toggle.length) {
			$toggle.attr('aria-expanded', 'false');
		}
	});

	// Initialize collapse state on page load
	$categoryTree.find('.collapse').each(function() {
		const $collapse = $(this);
		const collapseId = $collapse.attr('id');
		const $toggle = $categoryTree.find('[data-target="#' + collapseId + '"]');
		
		if ($toggle.length) {
			// Check if collapse is shown (has 'show' or 'in' class, or is visible)
			const isExpanded = $collapse.hasClass('show') || $collapse.hasClass('in') || $collapse.is(':visible');
			$toggle.attr('aria-expanded', isExpanded ? 'true' : 'false');
		}
	});

	// Fallback: Manual toggle if Bootstrap collapse isn't working
	$categoryTree.on('click', '.collapse-icons', function(e) {
		e.preventDefault();
		const $toggle = $(this);
		const target = $toggle.attr('data-target');
		
		if (!target) {
			return;
		}

		const $target = $(target);
		
		if (!$target.length) {
			return;
		}

		// Try Bootstrap collapse first
		if (typeof $.fn.collapse !== 'undefined') {
			$target.collapse('toggle');
		} else {
			// Fallback: manual toggle
			const isExpanded = $toggle.attr('aria-expanded') === 'true';
			
			if (isExpanded) {
				$target.slideUp(300);
				$toggle.attr('aria-expanded', 'false');
			} else {
				$target.slideDown(300);
				$toggle.attr('aria-expanded', 'true');
			}
		}
	});
}
