'use strict';
var log = function log() {
    console.log.apply(console, arguments);
};

// 检测浏览器版本
var browser = {
    // 判断浏览器类型
    versions: function () {
        var u = navigator.userAgent;
        var app = navigator.appVersion;
        return { //移动终端浏览器版本信息
            trident: u.indexOf('Trident') > -1, //IE内核
            presto: u.indexOf('Presto') > -1, //opera内核
            webKit: u.indexOf('AppleWebKit') > -1, //苹果、谷歌内核
            gecko: u.indexOf('Gecko') > -1 && u.indexOf('KHTML') == -1, //火狐内核
            mobile: !!u.match(/AppleWebKit.*Mobile.*/), //是否为移动终端
            ios: !!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/), //ios终端
            android: u.indexOf('Android') > -1 || u.indexOf('Linux') > -1, //android终端或者uc浏览器
            iPhone: u.indexOf('iPhone') > -1, //是否为iPhone或者QQHD浏览器
            iPad: u.indexOf('iPad') > -1, //是否iPad
            webApp: u.indexOf('Safari') == -1 //是否web应该程序，没有头部与底部
        };
    }(),
    language: (navigator.browserLanguage || navigator.language).toLowerCase()

    // 第一页轮播图
};var skipToNextIntro = function skipToNextIntro() {
    var currentSlide = $('.intro .intro-slide.current');
    currentSlide.removeClass('current');
    currentSlide.find('.text').css('visibility', 'hidden');
    var index = currentSlide.data('index');
    var next = parseInt(index) + 1;
    if (next >= $('.intro .intro-slide').length) {
        next = 0;
    }
    var nextSlide = $('.intro .intro-slide').eq(next);
    nextSlide.find('.text').css({ visibility: 'inherit' });
    nextSlide.addClass('current');
};
var skipToPrevIntro = function skipToPrevIntro() {
    var currentSlide = $('.intro .intro-slide.current');
    currentSlide.removeClass('current');
    currentSlide.find('.text').css('visibility', 'hidden');
    var index = currentSlide.data('index');
    var prev = parseInt(index) - 1;
    if (prev < 0) {
        prev = $('.intro .intro-slide').length - 1;
    }
    var prevSlide = $('.intro .intro-slide').eq(prev);
    prevSlide.find('.text').css({ visibility: 'inherit' });
    prevSlide.addClass('current');
};
// intro 轮播图控制
var introSlider = function introSlider() {
    var interval = 9000;
    var tid = 0;
    $('.intro .left').on('click', function (e) {
        // log('click left ', console.time())
        if (tid) {
            clearInterval(tid)
            tid = setInterval(function () {
                skipToNextIntro();
            }, interval);
        }
        skipToPrevIntro();
    });
    $('.intro .right').on('click', function (e) {
        // log('click right')
        if (tid) {
            clearInterval(tid)
            tid = setInterval(function () {
                skipToNextIntro();
            }, interval);
        }
        skipToNextIntro();
    });
    tid = setInterval(function () {
        skipToNextIntro();
    }, interval);
};

// 公司新闻动态
var createNewHtml = function createNewHtml(data) {
    var r = '';
    for (var i = 0; i < data.length; i++) {
        var item = data[i];
        var first = '';
        if (i === 0) {
            var first = 'current';
        }
        var t = '<div class="content-item ' + first + '" data-index="' + i + '">\n                    <div class="cover-wrapper">\n                        <img src="' + item.cover + '" alt="" title="" width="100%">\n                    </div>\n                    <div class="text-wrapper">\n                        <h3 class="title">' + item.title + '</h3>\n                        <div class="time">' + item.time + '</div>\n                        <p class="desc">' + item.desc + '</p>\n                        <a href="' + item.link + '">\n                            <button class="more-btn">\u4E86\u89E3\u8BE6\u60C5</button>\n                        </a>\n                    </div>\n                </div>';
        r += t;
    }
    return r;
};

var createNewSlider = function createNewSlider(data) {
    var r = '\n        <div class="news-slide-wrapper">\n            <a class="news-slide-prev"></a>\n            <a class="news-slide-next"></a>\n            <ul>\n        ';
    for (var i = 0; i < data.length; i++) {
        var cover = data[i].cover;
        var t = '<li data-index="' + i + '"><img src="' + cover + '" alt="" width="100%"></li>';
        r += t;
    }
    r += '\n            </ul>\n        </div>';
    return r;
};

var skipToNextNews = function skipToNextNews() {
    var currentNews = $('.news .content-item.current');
    var currentIndex = currentNews.data('index');
    currentNews.removeClass('current');
    var nextIndex = parseInt(currentIndex) + 1;
    if (nextIndex >= $('.news .content-item').length) {
        nextIndex = 0;
    }
    //
    $('.news .content-item:eq(' + nextIndex + ')').addClass('current');
    //
    $('.news li.current').removeClass('current');
    $('.news .slide-wrapper li:eq(' + nextIndex + ')').addClass('current');
};
var skipToPrevNews = function skipToPrevNews() {
    var currentNews = $('.news .content-item.current');
    var currentIndex = currentNews.data('index');
    currentNews.removeClass('current');
    var prevIndex = parseInt(currentIndex) - 1;
    if (prevIndex < 0) {
        prevIndex = $('.news .content-item').length - 1;
    }
    //
    $('.news .content-item:eq(' + prevIndex + ')').addClass('current');
    //
    $('.news li.current').removeClass('current');
    $('.news .slide-wrapper li:eq(' + prevIndex + ')').addClass('current');
};
// 待接口
var initNewsSlider = function initNewsSlider() {
    $('.news-slide-prev').on('click', function (e) {
        skipToPrevNews();
    });
    $('.news-slide-next').on('click', function (e) {
        skipToNextNews();
    });
    $('.news-slide-wrapper').on('click', 'li', function () {
        var index = $(this).data('index');
        log('轮播刷新', index);
        $('.news .content-item.current').removeClass('current');
        $('.news .content-item:eq(' + index + ')').addClass('current');
        $('.news li.current').removeClass('current');
        $('.news .slide-wrapper li:eq(' + index + ')').addClass('current');
    })
};
var initNewsOnMobile = function initNewsOnMobile() {
};

// 页面动画效果控制
var solutionBgTransform = function solutionBgTransform() {
    // $('.solution ul').on('mouseover', function (event) {
    //     var self = $(event.target);
    //     // log('hover', self, self.hasClass('content'))
    //     if (self.hasClass('content')) {
    //         var index = self.data('index');
    //         $('.solution-bg .current').removeClass('current');
    //         $('.solution-bg .bg-' + index).addClass('current');
    //     }
    // });
};

var pageInit = function pageInit() {
    $('header').addClass('suspend');
    $('.solution').removeClass('show');
    $('.news').removeClass('show');
};

$(".ma-infinitypush-wrapper").ontouchstart = function(e){ e.preventDefault(); }
var pageAnimation = function pageAnimation(startIndex, endIndex, direction) {
    // log('swiper ', anchorLink, index)
    // 隐藏所有的动画
    pageInit();
    if (endIndex === 1) {
        $('header').removeClass('suspend');
    } else if (startIndex === 1 && endIndex === 2 && direction === 'down' || startIndex === 3 && endIndex === 2 && direction === 'up') {
        $('.solution').addClass('show');
    } else if (startIndex === 2 && endIndex === 3 && direction === 'down' || startIndex === 4 && endIndex === 3 && direction === 'up') {
        $('.news').addClass('show');
    }
};

// 手机 header 侧滑功能
var suspendOpen = function suspendOpen() {
    $('#header .menu-toggle').on('click', function (e) {
        var menu = $('#header .menu');
        if (menu.hasClass('open')) {
            menu.removeClass('open');
        } else {
            menu.addClass('open');
        }
    });
};

//
var main = function main() {
    if (browser.versions.mobile) {
        //移动端打开此页面，不加载内容
        // window.alert('您用的是手机登陆')
        // initNewsOnMobile();
        $('section.solution').addClass('show');
        $('section.news').addClass('show');
        $('.menu-btn').on('click', function () {
            if ($('.menu-con').hasClass('open')) {
                $('.menu-con').removeClass('open');
            } else {
                $('.menu-con').addClass('open');
            }
        });
        introSlider();
        initNewsSlider();
    } else {
        // 滚动页面设置
        $('#main').fullpage({
            anchors: ['page1', 'page2', 'page3', 'page4', 'page5'],
            menu: '#menu',
            onLeave: pageAnimation
        });
        introSlider();
        solutionBgTransform();
        initNewsSlider();
        suspendOpen();
        var hash = window.location.hash;
        if (hash === '#page2') {
            setTimeout(function () {
                $('.solution').addClass('show');
            }, 1000);
        } else if (hash === '#page3') {
            setTimeout(function () {
                $('.news').addClass('show');
            }, 1000);
        }
    }
};
$(".other").click();

main();