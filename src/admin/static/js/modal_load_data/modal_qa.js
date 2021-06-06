$(function() {
	$(".view_icon").click(
		function() {
			var id = $(this).parents('.table_line_item').attr('data-id')
			var category = $(this).parents('.table_line_item').attr('data-category');
			var popular = $(this).parents('.table_line_item').attr('data-popular');
			var question = $(this).parents('.table_line_item').attr('data-question');
			var clear_question = $(this).parents('.table_line_item').attr('data-clear_question');
			var answer = $(this).parents('.table_line_item').attr('data-answer');
			var cat_id = $(this).parents('.table_line_item').attr('data-cat_id');

			$("#view_category_content").html(category);
			if (popular == "True") {
				star = '<span class="fa-stack"><i class="fa fa-star fa-stack-1x fa-lg"></i><i class="fa fa-star-o fa-stack-1x fa-lg"></i></span>';
			} else {
				star = '-';
			}
			$("#view_popular_content").html(star);
			$("#view_question_content").html(question);
			$("#view_clear_question_content").html(clear_question);
			$("#view_answer_content").html(answer);


			$("#viewModal").attr("data-id", id);
			$("#viewModal").attr("data-cat_id", cat_id);
			$("#viewModal").attr("data-popular", popular);
			$("#viewModal").attr("data-question", question);
			$("#viewModal").attr("data-answer", answer);
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

$(function() {
	$(".btn_view_edit").click(
		function() {
			var id = $("#viewModal").attr('data-id')
			var question = $("#viewModal").attr('data-question');
			var answer = $("#viewModal").attr('data-answer');
			var is_popular = $("#viewModal").attr('data-popular');
			var cat_id = $("#viewModal").attr('data-cat_id');

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
	$(".btn_view_delete").click(
		function() {
			var id = $("#viewModal").attr('data-id')
			var question = $("#viewModal").attr('data-question');

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