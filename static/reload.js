$.urlParam = function(name){
    var results = new RegExp('[/?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results==null){
       return null;
    }
    else{
       return decodeURI(results[1]) || 0;
    }
}
log = decodeURIComponent($.urlParam('login'))



function show(url, bl) {
    $.ajax({
        url : url,
        data : { login1: log},
        cache : false,
        success: function(html) {
                    bl.html(html);
        }
    });
  }

setInterval('show(\'/calls_today\', $(\'#calls_today\'))', 60000);
setInterval('show(\'/calls_month\', $(\'#calls_month\'))', 60000);
//исходящие
setInterval('show(\'/outcalls_today\', $(\'#outcalls_today\'))', 60000);
setInterval('show(\'/outcalls_month\', $(\'#outcalls_month\'))', 60000);

function show1() {
    $.ajax({
        url : '/top',
        cache : false,
        success: function(top1) {
                    var top_user = JSON.parse(top1);
                    $('#name1').html(top_user.name1);
                    $('#calls1').html(top_user.calls1);
                    $('#name2').html(top_user.name2);
                    $('#calls2').html(top_user.calls2);
                    $('#name3').html(top_user.name3);
                    $('#calls3').html(top_user.calls3);
        }
    });
    }
setInterval('show1()', 60000);




