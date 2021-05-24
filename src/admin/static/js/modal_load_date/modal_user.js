$(function() {
	$(".edit_icon").click(
		function() {
			var id = $(this).parents('.table_line_item').attr('data-id')
			var name = $(this).parents('.table_line_item').attr('data-name');
			var username = $(this).parents('.table_line_item').attr('data-username');
			var post = $(this).parents('.table_line_item').attr('data-post');

			$("#edit_id").val(id);
			$("#edit_name_content").val(name);
			$("#edit_username_content").val(username);
			$("#edit_post_content").val(post);
		})
});

$(function() {
	$(".delete_icon").click(
		function() {
			var id = $(this).parents('.table_line_item').attr('data-id');
			var name = $(this).parents('.table_line_item').attr('data-name');

			$("#delete_id").val(id);
			$("#delete_name_content").html(name);
		})
});

$(function() {
	$(".activate_icon").click(
		function() {
			var id = $(this).parents('.table_line_item').attr('data-id');
			var name = $(this).parents('.table_line_item').attr('data-name');

			$("#activate_id").val(id);
			$("#activate_name_content").html(name);
		})
});