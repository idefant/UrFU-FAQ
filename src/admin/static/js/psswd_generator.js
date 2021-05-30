$("#input-generate").click(function(){
	$("#input-password").val(generatePassword());
});

$("#change_password-generate").click(function(){
	$("#change_password").val(generatePassword());
});



function generatePassword(){
	var length = 16,
	charset = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz!?@+-/*_#$%&()[]{}";
	if(window.crypto && window.crypto.getRandomValues) {
		return Array(length)
		.fill(charset)
		.map(x => x[Math.floor(crypto.getRandomValues(new Uint32Array(1))[0] / (0xffffffff + 1) * (x.length + 1))])
		.join('');    
	} else {
		res = '';
		for (var i = 0, n = charset.length; i < length; ++i) {
			res += charset.charAt(Math.floor(Math.random() * n));
		}
		return res;
	}
}


$("#input-confirm").click(function(){
	if ($("#input-password").attr("type") === "text") {
		$("#input-password").attr('type','password');
		$("#input-confirm-password").removeAttr("readonly");
	}
	else if ($("#input-password").attr("type") === "password") {
		$("#input-password").attr('type','text');
		$("#input-confirm-password").attr('readonly', 'readonly');
		$("#input-confirm-password").val("");
	}
	
});




$(function() {
	$("#btn_change_psswd").click(
		function() {
			$("#old_password").val("");
			$("#input-password").val("");
			$("#input-confirm-password").val("");
			$("#input-confirm-password").attr('readonly', 'readonly');
		})
});