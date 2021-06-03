$(function() {
	$(".edit_icon").click(
		function() {
			var id = $(this).parents('.table_line_item').attr('data-id')
			var name = $(this).parents('.table_line_item').attr('data-name');
			var right_category = $(this).parents('.table_line_item').attr('data-right-category');
			var right_users = $(this).parents('.table_line_item').attr('data-right-users');
			var right_qa = $(this).parents('.table_line_item').attr('data-right-qa');
			var right_synonym = $(this).parents('.table_line_item').attr('data-right-synonym');
			var right_exception_word = $(this).parents('.table_line_item').attr('data-right-black_word');
			var right_request = $(this).parents('.table_line_item').attr('data-right-request');

			$("#edit_id").val(id);
			$("#user_rights_content").html(name);

			if (right_category == "True") {
				$("#edit_right_category").attr("checked","checked");
			} else {
				$("#edit_right_category").removeAttr("checked");
			}

			if (right_users == "True") {
				$("#edit_right_users").attr("checked","checked");
			} else {
				$("#edit_right_users").removeAttr("checked");
			}

			if (right_qa == "True") {
				$("#edit_right_qa").attr("checked","checked");
			} else {
				$("#edit_right_qa").removeAttr("checked");
			}

			if (right_synonym == "True") {
				$("#edit_right_synonym").attr("checked","checked");
			} else {
				$("#edit_right_synonym").removeAttr("checked");
			}

			if (right_exception_word == "True") {
				$("#edit_right_exception_word").attr("checked","checked");
			} else {
				$("#edit_right_exception_word").removeAttr("checked");
			}
			
			if (right_request == "True") {
				$("#edit_right_request").attr("checked","checked");
			} else {
				$("#edit_right_request").removeAttr("checked");
			}
		})
});