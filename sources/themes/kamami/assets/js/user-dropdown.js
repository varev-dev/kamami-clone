/**
 * User Info Dropdown & Login
 */
$(document).ready(function () {
	var $userInfo = $("#_desktop_user_info");

	// Show dropdown on hover (desktop only)
	$userInfo.on("mouseenter", function () {
		if ($(window).width() >= 768) {
			$(this).addClass("active");
		}
	});

	$userInfo.on("mouseleave", function () {
		if ($(window).width() >= 768 && !$(this).find("input:focus").length) {
			$(this).removeClass("active");
		}
	});

	// Keep open while typing
	$userInfo.on("focus", "input", function () {
		$userInfo.addClass("active");
	});

	$userInfo.on("focusout", "input", function () {
		setTimeout(function () {
			if (!$userInfo.find("input:focus").length) {
				$userInfo.removeClass("active");
			}
		}, 100);
	});

	// Close on ESC
	$(document).on("keyup", function (e) {
		if (e.keyCode === 27) {
			$userInfo.removeClass("active");
			$(".ets_solo_social_wrapper").removeClass("active");
		}
	});

	// Close button (mobile)
	$(document).on("click", ".ets_solo_account_close", function () {
		$(this).closest(".ets_solo_social_wrapper").removeClass("active");
	});

	// AJAX Login
	$("#header-login-form").on("submit", function (e) {
		e.preventDefault();

		var $form = $(this);
		var $btn = $form.find("button[type=submit]");
		var $errors = $form.find(".login-errors");

		if (!$errors.length) {
			$errors = $('<div class="login-errors"></div>').prependTo($form);
		}

		$errors.empty();
		$btn.prop("disabled", true);

		$.post($form.attr("action"), $form.serialize(), function (html) {
			var $alertDanger = $(html).find(".alert-danger");

			if ($alertDanger.length) {
				$alertDanger.each(function () {
					var text = $(this).text().trim();
					if (text) {
						$errors.append(
							'<div class="alert alert-danger">' + text + "</div>",
						);
					}
				});
				$btn.prop("disabled", false);
			} else {
				window.location.reload();
			}
		}).fail(function () {
			$errors.html(
				'<div class="alert alert-danger">Login failed. Please try again.</div>',
			);
			$btn.prop("disabled", false);
		});
	});
});
