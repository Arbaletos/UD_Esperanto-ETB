/* http://keith-wood.name/svg.html
   SVG/jQuery DOM compatibility for jQuery v1.4.3.
   Written by Keith Wood (kbwood{at}iinet.com.au) April 2009.
   Dual licensed under the GPL (http://dev.jquery.com/browser/trunk/jquery/GPL-LICENSE.txt) and 
   MIT (http://dev.jquery.com/browser/trunk/jquery/MIT-LICENSE.txt) licenses. 
   Please attribute the author if you use it. */
(function($){$.fn.addClass=function(e){return function(d){d=d||'';return this.each(function(){if(isSVGElem(this)){var c=this;$.each(d.split(/\s+/),function(i,a){var b=(c.className?c.className.baseVal:c.getAttribute('class'));if($.inArray(a,b.split(/\s+/))==-1){b+=(b?' ':'')+a;(c.className?c.className.baseVal=b:c.setAttribute('class',b))}})}else{e.apply($(this),[d])}})}}($.fn.addClass);$.fn.removeClass=function(e){return function(d){d=d||'';return this.each(function(){if(isSVGElem(this)){var c=this;$.each(d.split(/\s+/),function(i,a){var b=(c.className?c.className.baseVal:c.getAttribute('class'));b=$.grep(b.split(/\s+/),function(n,i){return n!=a}).join(' ');(c.className?c.className.baseVal=b:c.setAttribute('class',b))})}else{e.apply($(this),[d])}})}}($.fn.removeClass);$.fn.toggleClass=function(c){return function(a,b){return this.each(function(){if(isSVGElem(this)){if(typeof b!=='boolean'){b=!$(this).hasClass(a)}$(this)[(b?'add':'remove')+'Class'](a)}else{c.apply($(this),[a,b])}})}}($.fn.toggleClass);$.fn.hasClass=function(d){return function(b){b=b||'';var c=false;this.each(function(){if(isSVGElem(this)){var a=(this.className?this.className.baseVal:this.getAttribute('class')).split(/\s+/);c=($.inArray(b,a)>-1)}else{c=(d.apply($(this),[b]))}return!c});return c}}($.fn.hasClass);$.fn.attr=function(h){return function(b,c,d){if(typeof b==='string'&&c===undefined){var e=h.apply(this,[b,c,d]);if(e&&e.baseVal&&e.baseVal.numberOfItems!=null){c='';e=e.baseVal;for(var i=0;i<e.numberOfItems;i++){var f=e.getItem(i);switch(f.type){case 1:c+=' matrix('+f.matrix.a+','+f.matrix.b+','+f.matrix.c+','+f.matrix.d+','+f.matrix.e+','+f.matrix.f+')';break;case 2:c+=' translate('+f.matrix.e+','+f.matrix.f+')';break;case 3:c+=' scale('+f.matrix.a+','+f.matrix.d+')';break;case 4:c+=' rotate('+f.angle+')';break;case 5:c+=' skewX('+f.angle+')';break;case 6:c+=' skewY('+f.angle+')';break}}e=c.substring(1)}return(e&&e.baseVal?e.baseVal.valueAsString:e)}var g=b;if(typeof b==='string'){g={};g[b]=c}return this.each(function(){if(isSVGElem(this)){for(var n in g){var a=($.isFunction(g[n])?g[n]():g[n]);(d?this.style[n]=a:this.setAttribute(n,a))}}else{h.apply($(this),[b,c,d])}})}}($.fn.attr);$.fn.removeAttr=function(b){return function(a){return this.each(function(){if(isSVGElem(this)){(this[a]&&this[a].baseVal?this[a].baseVal.value='':this.setAttribute(a,''))}else{b.apply($(this),[a])}})}}($.fn.removeAttr);function anySVG(a){for(var i=0;i<a.length;i++){if(a[i].nodeType==1&&a[i].namespaceURI==$.svg.svgNS){return true}}return false}$.expr.relative['+']=function(d){return function(a,b,c){d(a,b,c||anySVG(a))}}($.expr.relative['+']);$.expr.relative['>']=function(d){return function(a,b,c){d(a,b,c||anySVG(a))}}($.expr.relative['>']);$.expr.relative['']=function(d){return function(a,b,c){d(a,b,c||anySVG(a))}}($.expr.relative['']);$.expr.relative['~']=function(d){return function(a,b,c){d(a,b,c||anySVG(a))}}($.expr.relative['~']);$.expr.find.ID=function(d){return function(a,b,c){return(isSVGElem(b)?[b.ownerDocument.getElementById(a[1])]:d(a,b,c))}}($.expr.find.ID);var j=document.createElement('div');j.appendChild(document.createComment(''));if(j.getElementsByTagName('*').length>0){$.expr.find.TAG=function(a,b){var c=b.getElementsByTagName(a[1]);if(a[1]==='*'){var d=[];for(var i=0;c[i]||c.item(i);i++){if((c[i]||c.item(i)).nodeType===1){d.push(c[i]||c.item(i))}}c=d}return c}}$.expr.preFilter.CLASS=function(a,b,c,d,f,g){a=' '+a[1].replace(/\\/g,'')+' ';if(g){return a}for(var i=0,elem={};elem!=null;i++){elem=b[i];if(!elem){try{elem=b.item(i)}catch(e){}}if(elem){var h=(!isSVGElem(elem)?elem.className:(elem.className?elem.className.baseVal:'')||elem.getAttribute('class'));if(f^(h&&(' '+h+' ').indexOf(a)>-1)){if(!c)d.push(elem)}else if(c){b[i]=false}}}return false};$.expr.filter.CLASS=function(a,b){var c=(!isSVGElem(a)?a.className:(a.className?a.className.baseVal:a.getAttribute('class')));return(' '+c+' ').indexOf(b)>-1};$.expr.filter.ATTR=function(g){return function(c,d){var e=null;if(isSVGElem(c)){e=d[1];$.expr.attrHandle[e]=function(a){var b=a.getAttribute(e);return b&&b.baseVal||b}}var f=g(c,d);if(e){$.expr.attrHandle[e]=null}return f}}($.expr.filter.ATTR);function isSVGElem(a){return(a.nodeType==1&&a.namespaceURI==$.svg.svgNS)}})(jQuery);