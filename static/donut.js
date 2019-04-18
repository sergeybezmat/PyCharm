function chart(name, data1, data2) {

    new Chart(document.getElementById(name), {
        type: 'doughnut',
        data: {

            datasets: [
                {

                    backgroundColor: ["#FFB500", "#CED3C8"],
                    data: [data1, data2-data1]
                }
            ]
        },
        options: {
            cutoutPercentage: 90,
            elements: {
                center: {
                    text: data1 + '/' + data2,
                    fontStyle: 'Helvetica', //Default Arial
                    sidePadding: 15, //Default 20 (as a percentage)
                    maintainAspectRatio: true,
                    responsive: false
                }
            }
        }
    });
}