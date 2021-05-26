let tabButtons = document.querySelectorAll(".tabs-menu button");
let tabPanels = document.querySelectorAll(".tab-content");

function showPanel(panelIndex) {
	tabButtons.forEach(function(node) {
		node.classList.remove('current');
	});
	tabPanels.forEach(function(node) {
		node.style.display="none";
	});
	tabPanels[panelIndex].style.display="block";
	tabButtons[panelIndex].classList.add('current');

	$('.tab-content-container').masonry({
		itemSelector: '.qa_item',
		transitionDuration: 0
	});
}



$(function() {
	$("#pure-toggle-right").click(
		function() {
			if ($("#pure-toggle-right").is(":checked"))
			{
				$('html').css("overflow", "hidden");
			}
			else
			{
				$('html').css("overflow", "visible");
			}
		})
});