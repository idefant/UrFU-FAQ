function setAttr(prmName,val){
	var res = '';
	var d = location.href.split("#")[0].split("?");
	var base = d[0];
	var query = d[1];
	if(query) {
		var params = query.split("&");
		for(var i = 0; i < params.length; i++) {
			var keyval = params[i].split("=");
			if(keyval[0] != prmName) {
				res += params[i];
			}
		}
	}
	if (val.length != 0)
	{
		if (res.length != 0)
			res += '&';
		res += prmName + '=' + val;
		window.location.href = base + '?' + res;
		
	} else {
		if (res.length == 0) {
			window.location.href = base
		} else {
			window.location.href = base + '?' + res;
		}
		
	}
	return false;
}