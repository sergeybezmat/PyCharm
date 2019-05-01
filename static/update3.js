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

function chart(name, data1, data2) {

    new Chart(document.getElementById(name), {
        type: 'doughnut',
        data: {

            datasets: [
                {

                    backgroundColor: ["#FFB500", "#CED3C8"],
                    data: [data1, data2 - data1]
                }
            ]
        },
        options: {
            animation: false,
            cutoutPercentage: 67,
            tooltips: {enabled: false},
            hover: {mode: null},
            elements: {
                center: {
                    text: data1 + '/' + data2,
                    fontStyle: 'Helvetica', //Default Arial
                    fontSize: 1,
                    sidePadding: 15, //Default 20 (as a percentage)
                    maintainAspectRatio: true,
                    responsive: false
                }
            }
        }
    });
}
var plan_calls1 = $('#plan_calls').html();
var plan_outcalls1 = $('#plan_outcalls').html();
var plan_month = plan_calls1 * 21,
    plan_month_out = plan_outcalls1 * 21;

function calls_all() {
    $.ajax({
        url : '/calls_all',
        data : { login1: log},
        cache : false,
        success: function(calls_all) {
                    var calls = JSON.parse(calls_all);
                         chart('incall_yest', calls.outcalls_yest,plan_outcalls1);
                         chart('incall_today', calls.outcalls_today,plan_outcalls1);
                         chart('outcall_yest', calls.calls_yest,plan_calls1);
                         chart('outcall_today', calls.calls_today,plan_calls1);
                         chart('incall_month', calls.outcalls_month,plan_month_out);
                         chart('outcall_month', calls.calls_month,plan_month);
        }
    });
}

function top3() {
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
top3();
setInterval('top3()', 60000);

calls_all();
setInterval('calls_all()', 60000);