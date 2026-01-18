/**
 * DropDown - Animated dropdown component
 * Handles currency selector, language selector, and other dropdowns with slide animations
 *
 * @example
 * const dropdown = new DropDown($(".js-dropdown"));
 * dropdown.init();
 */
class DropDown {
	constructor(el) {
		this.el = el;
		this.animationDuration = 200;
	}

	init() {
		this._bindShowEvent();
		this._bindHideEvent();
		this._bindMobileSelect();
		this._bindToggleClick();
		this._bindOutsideClick();
	}

	_bindShowEvent() {
		this.el.on("show.bs.dropdown", (e, t) => {
			(t ? $(`#${t}`) : $(e.target))
				.find(".dropdown-menu")
				.first()
				.stop(true, true)
				.slideDown(this.animationDuration);
		});
	}

	_bindHideEvent() {
		this.el.on("hide.bs.dropdown", (e, t) => {
			(t ? $(`#${t}`) : $(e.target))
				.find(".dropdown-menu")
				.first()
				.stop(true, true)
				.slideUp(this.animationDuration);
		});
	}

	_bindMobileSelect() {
		this.el.find("select.link").each((_, element) => {
			$(element).on("change", function () {
				window.location = $(this).val();
			});
		});
	}

	_bindToggleClick() {
		const self = this;

		this.el.find('[data-toggle="dropdown"]').on("click", function (e) {
			e.preventDefault();
			e.stopPropagation();

			const $parent = $(this).closest(".js-dropdown");
			const $menu = $parent.find(".dropdown-menu").first();
			const isOpen = $parent.hasClass("open");

			// Close all other dropdowns first
			self._closeAllExcept($parent);

			// Toggle this dropdown
			if (isOpen) {
				self._closeDropdown($parent, $menu);
			} else {
				self._openDropdown($parent, $menu);
			}
		});
	}

	_bindOutsideClick() {
		const self = this;

		$(document).on("click", (e) => {
			if (!$(e.target).closest(".js-dropdown").length) {
				self._closeAll();
			}
		});
	}

	_openDropdown($parent, $menu) {
		$parent.addClass("open");
		$menu.hide().stop(true, true).slideDown(this.animationDuration);
	}

	_closeDropdown($parent, $menu) {
		$menu.stop(true, true).slideUp(this.animationDuration, () => {
			$parent.removeClass("open");
		});
	}

	_closeAllExcept($exclude) {
		$(".js-dropdown.open")
			.not($exclude)
			.each((_, element) => {
				const $parent = $(element);
				const $menu = $parent.find(".dropdown-menu").first();
				this._closeDropdown($parent, $menu);
			});
	}

	_closeAll() {
		$(".js-dropdown.open").each((_, element) => {
			const $parent = $(element);
			const $menu = $parent.find(".dropdown-menu").first();
			this._closeDropdown($parent, $menu);
		});
	}
}
