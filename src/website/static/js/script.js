let tabButtons = document.querySelectorAll(".tabs-menu button");
let tabPanels = document.querySelectorAll(".tab-content");

function showPanel(panelIndex, buttonIndex) {

	tabButtons.forEach(function(node) {
		node.classList.remove('current');
	});
	tabPanels.forEach(function(node) {
		node.style.display="none";
	});
	tabPanels[panelIndex].style.display="block";
	tabButtons[buttonIndex].classList.add('current');

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
			} else {
				$('html').css("overflow", "visible");
			}
		})
});



var scrollingAnimate = function (offsetTop) {
			$('html, body').stop().animate({
				scrollTop: parseInt(offsetTop) || 0
			}, 500);
		};

		var checkPageUpButton = function () {
			var pageUP = $('#page_up');
			if ( pageUP.css('display') != 'block' && $(window).scrollTop() > ($(window).height() / 3)){
				pageUP.fadeIn().css('display', 'block');
			}
			if ( pageUP.css('display') != 'none' && $(window).scrollTop() < ($(window).height() / 3)){
				pageUP.fadeIn().css('display', 'none');
			}
		};


		$('#page_up').on('click', scrollingAnimate);
		setInterval(checkPageUpButton, 500);