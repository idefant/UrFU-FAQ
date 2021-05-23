$(document).ready(function() {
	$('.summernote').summernote({
		lang:'ru-RU',
		height:300,
		minHeight:200,
		maxHeight:500,
		disableDragAndDrop:false,
		shortcuts: false,
		tabDisable: false,
		codeviewFilter: false,
		codeviewIframeFilter: true,
		toolbar: [
		['style', ['bold', 'underline', 'clear']],
		['para', ['ul', 'ol']],
		['insert', ['link']],
		['misc', ['undo', 'redo']]
		]
	});
	$('#edit_answer_content').summernote('insertText', '');
});