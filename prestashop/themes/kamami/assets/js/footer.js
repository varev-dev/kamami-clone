/**
 * Simple footer scroll-to-top button
 */

(function () {
	const goTopBtn = document.getElementById("go_top");

	if (!goTopBtn) return;

	// Show/hide button on scroll
	window.addEventListener("scroll", function () {
		if (window.scrollY > 300) {
			goTopBtn.classList.add("visible");
		} else {
			goTopBtn.classList.remove("visible");
		}
	});

	// Scroll to top on click
	goTopBtn.addEventListener("click", function (e) {
		e.preventDefault();
		window.scrollTo({ top: 0, behavior: "smooth" });
	});
})();
