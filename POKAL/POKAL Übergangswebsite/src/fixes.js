/**
 * POKAL-Uebergangsseite. Lauter Code um Sachen zu realisieren, die mit
 * CSS3 fast schon gehen.
 *
 **/

function min(a,b) { return a > b ? b : a; }
function max(a,b) { return b > a ? b : a; }

function fixsizes() {
	w = $(banner).width(); h = $(banner).height();
	iw = 1600; ih = 1200; // initial picture sizes
	scale = max(w/iw, h/ih);
	console.log(w,h,scale);
	
	$(links).each(function(){
		$(this).css({
			left: $(banner).position().left +  scale*ipos[this].left+"px",
			top: scale*ipos[this].top+"px",
			width: scale*iwidth[this]+"px",
			height: scale*iheight[this]+"px"
		});
	});
}

ipos = {}; iwidth = {}; iheight= {};
links = "#logo, #self, #pe, #uni";
banner = "#banner"
imgpath = "src/hot.%ID.jpg";

$(function(){
	$(window).resize(fixsizes).load(fixsizes);
	$("html").removeClass("no-js").addClass("js");
	
	// store initial positions
	$(links).add(banner).each(function(){
		ipos[this] = $(this).position();
		iwidth[this]= $(this).width();
		iheight[this] = $(this).height();
	});

	// make code corrections
	$("#banner").unwrap(); // remove outer <a>
	$(links).each(function(){
		$(this).wrapInner("<span/>").css("background-image", "none"); // to hide text labels
		$("<img>").attr("src", imgpath.replace(/%ID/, this.id)).appendTo(this);
	});
});