//scrolling function

// h5
function scrollToElement(elementId,speed){
	let destEle = document.getElementById(elementId);
    let scrolltopTemp = document.documentElement.scrollTop || document.body.scrollTop;
    //let rect = destEle.getBoundingClientRect();
    // 获取元素相对窗口的top值，此处应加上页面本身的偏移
    let top = scrolltopTemp + 20;
    let currentTop = 0;
    let requestId;
    // 采用requestAnimationFrame，平滑动画
    function step () {
        currentTop += speed;
        if (currentTop <= top) {
            document.body.scrollTo(0, currentTop);
            requestId = window.requestAnimationFrame(step);
        } else {
            window.cancelAnimationFrame(requestId);
        }
    }
    window.requestAnimationFrame(step);
}