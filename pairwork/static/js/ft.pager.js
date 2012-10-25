function changeday(){
	window.location=document.getElementById("daylist").value;	
}
function gopage(total){
	var curlurl = document.URL
	var urllist = curlurl.split('?');
	var pagestr = document.getElementById("page").value
	var page = parseInt(pagestr);
	if (isNaN(page)){
		page = 1;
	}else{
		if(page>total){
			page = total;
		}else if(page<1){
		    page = 1;
		}
	}
	if(location.search.indexOf('page')>-1){
		var page_start_index = curlurl.indexOf('page');
		var page_end_string = curlurl.substring(page_start_index, curlurl.length)
		if(page_end_string.indexOf("&")>-1){
			page_end_index = page_start_index + curlurl.substring(page_start_index, curlurl.length).indexOf("&");
		}else{
			page_end_index = curlurl.length
		}
		window.location.href = curlurl.substring(0, page_start_index) + 'page='+ page + curlurl.substring(page_end_index, curlurl.length);
	}else{
		if (urllist.length == 1){
			window.location.href = curlurl + '?page='+page;
		
		}else{
			window.location.href = curlurl + '&page='+page;		
		}
	}
}
function clickpage(page){
	var curlurl = document.URL;
	var urllist = curlurl.split('?');
	if(location.search.indexOf('page')>-1){
		var page_start_index = curlurl.indexOf('page');
		var page_end_string = curlurl.substring(page_start_index, curlurl.length)
		if(page_end_string.indexOf("&")>-1){
			page_end_index = page_start_index + curlurl.substring(page_start_index, curlurl.length).indexOf("&");
		}else{
			page_end_index = curlurl.length;
		}
		window.location.href = curlurl.substring(0, page_start_index) + 'page='+ page + curlurl.substring(page_end_index, curlurl.length);
	}else{
		if (urllist.length == 1){
			window.location.href = curlurl + '?page='+page;
		
		}else{
			window.location.href = curlurl + '&page='+page;
		}
	}
}

function chgColor(select){
	select.style.background = select[select.selectedIndex].style.background;
}

function sortTable(value){
	if (value == 'link'){
		return;
	}
	var curlurl = document.URL
	var urllist = curlurl.split('?');
	if(location.search.indexOf('sort')>-1){
		var column_index = curlurl.indexOf('sort');
		var type_index = curlurl.indexOf('orderby')+'orderby'.length+1;
		var orderby = curlurl.substring(type_index, type_index+1)
		if (location.search.indexOf(value)>-1 ){
			if(parseInt(orderby)==0){
				orderby = 1;
			}else{
				orderby = 0;
			}
		}else{
			orderby = 0;
		}
		window.location.href = curlurl.substring(0, column_index)+ 'sort='+ value + ';orderby='+orderby;		
	}else{
		if (urllist.length == 1){
			window.location.href = curlurl + '?sort='+value + ';orderby=0';
		
		}else{
			window.location.href = curlurl + ';sort='+value + ';orderby=0';		
		}		
	}		
}

function searchSubmit(searchurl){
	var searchVaule = document.getElementById('searchVaule').value;
	if(searchVaule!=''){
		window.location.href=searchurl+'/'+searchVaule;
	}
}

