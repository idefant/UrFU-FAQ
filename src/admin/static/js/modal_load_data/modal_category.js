$(function() {
	$(".edit_icon").click(
		function() {
			var id = $(this).parents('.table_line_item').attr('data-id')
			var name = $(this).parents('.table_line_item').attr('data-name');
			var icon_name = $(this).parents('.table_line_item').attr('data-icon_name');

			$("#edit_id").val(id);
			$("#edit_name_content").val(name);
			$("#edit_icon_name_content").val(icon_name);
		})
});

$(function() {
	$(".delete_icon").click(
		function() {
			var id = $(this).parents('.table_line_item').attr('data-id');
			var count_qa = $(this).parents('.table_line_item').attr('data-count_qa');
			var name = $(this).parents('.table_line_item').attr('data-name');

			$("#delete_id").val(id);
			$("#delete_count_qa").val(count_qa);
			$("#delete_name_content").html(name);
		})
});