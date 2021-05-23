$(function() {
	$(".edit_icon").click(
		function() {
			var id = $(this).parents('.table_line_item').attr('data-id')
			var name = $(this).parents('.table_line_item').attr('data-name');
			var right_category = $(this).parents('.table_line_item').attr('data-right-category');
			var right_users = $(this).parents('.table_line_item').attr('data-right-users');

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
		})
});