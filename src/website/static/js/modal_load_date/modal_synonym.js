$(function() {
	$(".edit_icon").click(
		function() {
			var id = $(this).parents('.table_line_item').attr('data-id')
			var name = $(this).parents('.table_line_item').attr('data-name');

			$("#edit_id").val(id);
			$("#edit_name_content").val(name);
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