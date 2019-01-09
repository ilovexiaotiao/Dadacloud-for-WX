// QRCODE reader Copyright 2011 Lazar Laszlo
// http://www.webqr.com

var gCtx = null;
var gCanvas = null;
var c=0;
var stype=0;
var gUM=false;
var webkit=false;
var moz=false;
var v=null;
var Param1="";
var filecookie="";
var getname="";
var piccookie="";
//var location="";

var imghtml='<div id="qrfile"><canvas id="out-canvas" width="320" height="240"></canvas>'+
    '<div id="imghelp">drag and drop a QRCode here'+
	'<br>or select a file'+
	'<form action="" method="post" id="form1" enctype="multipart/form-data">'+
	'<input type="file" name="file" id="file" onchange="handleFiles(this.files);"/>'+
	'<input type="submit" id="autosubmit" value="upload"/>'+
	'</form>'+
	'<iframe id="framenone" name="id_iframe" style="display:none;"></iframe>'+
	'</div>'+
'</div>';
var vidhtml = '<video id="v" autoplay></video>';





function dragenter(e) {
  e.stopPropagation();
  e.preventDefault();
}

function dragover(e) {
  e.stopPropagation();
  e.preventDefault();
}
function drop(e) {
  e.stopPropagation();
  e.preventDefault();

  var dt = e.dataTransfer;
  var files = dt.files;
  if(files.length>0)
  {
	handleFiles(files);
  }
  else
  if(dt.getData('URL'))
  {
	qrcode.decode(dt.getData('URL'));
  }
}



function handleFiles(f)
{
	var o=[];
	for(var i =0;i<f.length;i++)
	{
        var reader = new FileReader();
        reader.onload = (function(theFile) {
        return function(e) {
            gCtx.clearRect(0, 0, gCanvas.width, gCanvas.height);

			qrcode.decode(e.target.result);
        };
        })(f[i]);
        reader.readAsDataURL(f[i]);	
    }
    //alert(reader);
}

function initCanvas(w,h)
{
    gCanvas = document.getElementById("qr-canvas");
    gCanvas.style.width = w + "px";
    gCanvas.style.height = h + "px";
    gCanvas.width = w;
    gCanvas.height = h;
    gCtx = gCanvas.getContext("2d");
    gCtx.clearRect(0, 0, w, h);
}


function captureToCanvas() {
    if(stype!=1)
        return;
    if(gUM)
    {
        try{
            gCtx.drawImage(v,0,0);
            try{
                qrcode.decode();
            }
            catch(e){       
                console.log(e);
                setTimeout(captureToCanvas, 500);
            };
        }
        catch(e){       
                console.log(e);
                setTimeout(captureToCanvas, 500);
        };
    }
}

function htmlEntities(str) {
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function read(a)
{
    var html="";
    //if(a.indexOf("http://") === 0 || a.indexOf("https://") === 0)
    //    html+="<a target='_blank' href='"+a+"'>"+a+"</a><br>";
    //html+="<b>"+htmlEntities(a)+"</b><br><br>";
		html+=htmlEntities(a);
	var picname=document.getElementById("file").value.split("\\")[2]
		setCookie('filecookie',html);
		setCookie('piccookie',picname);
		//alert(html);
        document.getElementById("result").innerHTML=html;
        //alert(html);
		//window.open(fixedEncodeURI(html),'_self','');
		//alert(html);
		document.getElementById("form1").submit();
		//alert(document.getElementById("file").getContext) ;

}


//function savehtml(){

   // alert("savehtml");
  //  var getname=getCookie("filecookie");
   // var picname=document.getElementById("file").value.split("\\")[2]
   // var geturl=getname+"?"+picname;
    //alert(geturl);
    //alert(getCookie("filecookie"));
    //alert(getCookie("filecookie"));
   //alert(document.getElementById("file").value);
  //  if (getCookie("filecookie") != null&&getCookie("filecookie") != ""){
        //if (document.getElementById("file").value=!""){
         //   window.open(fixedEncodeURI(getname),'_self');
         //   setCookie("filecookie","",-1);
        //}
   // }

//}


function isCanvasSupported(){
  var elem = document.createElement('canvas');
  return !!(elem.getContext && elem.getContext('2d'));
}
function success(stream) {
    if(webkit)
        v.src = window.URL.createObjectURL(stream);
    else
    if(moz)
    {
        v.mozSrcObject = stream;
        v.play();
    }
    else
        v.src = stream;
    gUM=true;
    setTimeout(captureToCanvas, 500);
}
		
function error(error) {
    gUM=false;
    return;
}

function load()
{
	if(isCanvasSupported() && window.File && window.FileReader)
	{
		initCanvas(800, 600);
		qrcode.callback = read;
		document.getElementById("mainbody").style.display="inline";

	}
	else
	{
		document.getElementById("mainbody").style.display="inline";
		document.getElementById("mainbody").innerHTML='<p id="mp1">保洁签到</p><br>'+
        '<br><p id="mp2">sorry your browser is not supported</p><br><br>'+
        '<p id="mp1">try <a href="http://www.mozilla.com/firefox"><img src="firefox.png"/></a> or <a href="http://chrome.google.com"><img src="chrome_logo.gif"/></a> or <a href="http://www.opera.com"><img src="Opera-logo.png"/></a></p>';
	}
}


function setwebcam2(options)
{
	console.log(options);
	document.getElementById("result").innerHTML="- scanning -";
    if(stype==1)
    {
        setTimeout(captureToCanvas, 500);    
        return;
    }
    var n=navigator;
    document.getElementById("outdiv").innerHTML = vidhtml;
    v=document.getElementById("v");


    if(n.getUserMedia)
        n.getUserMedia({video: options, audio: false}, success, error);
    else
    if(n.webkitGetUserMedia)
    {
        webkit=true;
        n.webkitGetUserMedia({video:options, audio: false}, success, error);
    }
    else
    if(n.mozGetUserMedia)
    {
        moz=true;
        n.mozGetUserMedia({video: options, audio: false}, success, error);
    }

    //document.getElementById("qrimg").src="qrimg2.png";
    //document.getElementById("webcamimg").src="webcam.png";
    document.getElementById("qrimg").style.opacity=0.2;
    document.getElementById("webcamimg").style.opacity=1.0;

    stype=1;
    setTimeout(captureToCanvas, 500);
}

function setimg()
{
	  //document.getElementById("result").innerHTML="";
    //if(stype==2)
     //   return;
    document.getElementById("outdiv").innerHTML = imghtml;
    //document.getElementById("qrimg").src="qrimg.png";
    //document.getElementById("webcamimg").src="webcam2.png";
    //document.getElementById("qrimg").style.opacity=1.0;
    //document.getElementById("webcamimg").style.opacity=0.2;
    var qrfile = document.getElementById("qrfile");
    qrfile.addEventListener("dragenter", dragenter, false);  
    qrfile.addEventListener("dragover", dragover, false);  
    qrfile.addEventListener("drop", drop, false);
    stype=2;
}


function set_param1(a)
{
	var html="";
	var url="";
	//if(a.indexOf("http://") === 0 || a.indexOf("https://") === 0)
	//		url+="<a target='_blank' href='"+a+"'>"+a+"</a><br>";
	html+=htmlEntities(a);
	document.getElementById("result").innerHTML=html;
	setCookie('Param1',html)
}

function setCookie(name,value){  

var Days = 30;   //cookie 将被保存30天

var exp  = new Date();  //获得当前时间

exp.setTime(exp.getTime() + Days*24*60*60*1000);  //换成毫秒

document.cookie = name + "="+ value + ";expires=" + exp.toGMTString();

}   

function fixedEncodeURI (str) {
    return encodeURI(str).replace('&amp;', '&');
};


function getQueryString(name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
        var r = fixedEncodeURI(window.location).search.substr(1).match(reg);
        if (r != null) return unescape(r[2]);
        return null;
} ;

function setCookie(name, value, Days){
		if(Days == null || Days == ''){
			Days = 300;
		}
		var exp  = new Date();
		exp.setTime(exp.getTime() + Days*24*60*60*1000);
		document.cookie = name + "="+ escape (value) + "; path=/;expires=" + exp.toGMTString();
		//document.cookie = name + "="+ escape (value) + ";expires=" + exp.toGMTString();
	}

	/*get cookie*/
	function getCookie(name) {
		var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");
		if(arr=document.cookie.match(reg))
			return unescape(arr[2]);
		else
			return null;
	}
