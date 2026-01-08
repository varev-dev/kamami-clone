(function ($) {
	"use strict";

	$(document).ready(function () {
		$(document).on(
			"click",
			'button[data-action="show-password"]',
			function (e) {
				e.preventDefault();

				var $button = $(this);
				var $inputGroup = $button.closest(".input-group");
				var $passwordInput = $inputGroup.find(".js-visible-password");

				if ($passwordInput.length === 0) {
					return;
				}

				var currentType = $passwordInput.attr("type");
				var textShow = $button.data("text-show") || "Pokaż";
				var textHide = $button.data("text-hide") || "Ukryj";

				if (currentType === "password") {
					$passwordInput.attr("type", "text");
					$button.text(textHide);
				} else {
					$passwordInput.attr("type", "password");
					$button.text(textShow);
				}
			},
		);
	});
})(jQuery);
