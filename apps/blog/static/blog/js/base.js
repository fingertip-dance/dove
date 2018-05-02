//bootstrap4 tooltips
// $(function () {
//     $('[data-toggle="tooltip"]').tooltip()
// });
//回到顶部
$(window).scroll(function(){
    $('#to-top').hide();
    if ($(window).scrollTop()>=200){
        $('#to-top').show();
    };
});
$("#to-top").click(function () {
        var speed=400;//滑动的速度
        $('body,html').animate({ scrollTop: 0 }, speed);
        return false;
 });
//锚点平滑移动到指定位置
function TOC_FUN(A) {
	$(A).click(function() {
		$(A).css("color", "#000");
		$(this).css("color", "red");
		$('html, body').animate({
			scrollTop: $($.attr(this, 'href')).offset().top - 55
		}, 500);
		return false
	})
}
$(TOC_FUN('.toc a'));
