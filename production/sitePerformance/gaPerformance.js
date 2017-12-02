///add this script as close to the <head> element tag as possible
if(typeof sessionStorage !== "undefined"){
    sessionStorage.setItem('pageI',+ new Date());
}  
    
///add this script on the gtm.js event on all pages
if(typeof sessionStorage !== "undefined"){
  	sessionStorage.setItem('pageS',+ new Date());
    if(sessionStorage.getItem('sessionPageCount')!==null){
        var pageCount = parseInt(sessionStorage.getItem('sessionPageCount'))+1;
        sessionStorage.setItem('sessionPageCount',pageCount);
  	}
    else{
        sessionStorage.setItem('sessionPageCount',1);
    }
}

///add this script on the gtm.load event on all pages
if(typeof sessionStorage !== "undefined"){
    sessionStorage.setItem('pageE',+ new Date());
    var i = parseInt(sessionStorage.getItem('pageI'));
    var s = parseInt(sessionStorage.getItem('pageS')) - parseInt(sessionStorage.getItem('pageI'));
    var e = parseInt(sessionStorage.getItem('pageE')) - parseInt(sessionStorage.getItem('pageS'));
    var t;
    if(sessionStorage.getItem('sessionTotalLoadTime')!==null){
        t = e + parseInt(sessionStorage.getItem('sessionTotalLoadTime'));
    }
    else{
        sessionStorage.setItem('sessionTotalLoadTime', e);
        t = e;
    }
    var pc = parseInt(sessionStorage.getItem('sessionPageCount'));
    dataLayer.push({
        'event': 'pagePerform',
        'pageInit': i,
        'pageStart': s,
        'pageEnd': e,
        'pageTotal': s+e,
        'pageLoadDimension': String(Math.ceil((s+e)/100)*100/1000),
        'sessionPageCount': pc,
        'sessionLoadDimension': String(Math.ceil((t)/100)*100/1000),
        'sessionAvgPageLoadDimension': String(Math.ceil((t/pc)/100)*100/1000)
    });
}