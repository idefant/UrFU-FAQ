$(function() {
	$(".view_icon").click(
		function() {
			var category = $(this).parents('.table_line_item').attr('data-category');
			var popular = $(this).parents('.table_line_item').attr('data-popular');
			var question = $(this).parents('.table_line_item').attr('data-question');
			var answer = $(this).parents('.table_line_item').attr('data-answer');

			$("#view_category_content").html(category);
			var star = ""
			if (popular == "True") {
				star = '<span class="fa-stack"><i class="fa fa-star fa-stack-1x fa-lg"></i><i class="fa fa-star-o fa-stack-1x fa-lg"></i></span>';
			} else {
				star = '-';
			}
			$("#view_popular_content").html(star);
			$("#view_question_content").html(question);
			$("#view_answer_content").html(answer);
		})
});

$(function() {
	$(".edit_icon").click(
		function() {
			var id = $(this).parents('.table_line_item').attr('data-id')
			var question = $(this).parents('.table_line_item').attr('data-question');
			var answer = $(this).parents('.table_line_item').attr('data-answer');
			var is_popular = $(this).parents('.table_line_item').attr('data-popular');
			var cat_id = $(this).parents('.table_line_item').attr('data-cat_id');

			$("#edit_id").val(id);
			$("#edit_question_content").val(question);
			$('#edit_answer_content').summernote('insertText', '');
			$('#edit_answer_content').summernote('code', '');
			
			$('#edit_answer_content').summernote('pasteHTML', answer);
			if (is_popular == "True") {
				$("#edit_popular_content").attr("checked","checked");
			} else {
				$("#edit_popular_content").removeAttr("checked");
			}
			$("#edit_cat_id_content").val(cat_id);
		})
});

$(function() {
	$(".delete_icon").click(
		function() {
			var id = $(this).parents('.table_line_item').attr('data-id');
			var question = $(this).parents('.table_line_item').attr('data-question');

			$("#delete_id").val(id);
			$("#delete_question_content").html(question);
		})
});




var choosing_cat = $("#cat_id").attr('onchange', "checkParams()");
checkParams();

function checkParams() {
    var cat_id = $('#cat_id').val();
    if(cat_id != 0) {
        $('#submit').removeAttr('disabled');
    } else {
        $('#submit').attr('disabled', 'disabled');
    }
}