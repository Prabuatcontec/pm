$(document).ready(function() {
    $('#mob-gig-date-gteq').change(function() {
        var date = $(this).val();
        console.log(date, 'change')

        var today = new Date();
        var dd = String(today.getDate()).padStart(2, '0');
        var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
        var yyyy = today.getFullYear();
        ye = 0
        today = yyyy + '-' + mm + '-' + dd;

        if(date == today){
            ye = 1;
        }
        console.log(ye, 'change')
        var myDate = date;  
        myDate = myDate.split("-");
        var newDate = new Date( myDate[0], myDate[1] - 1, myDate[2]);

        startDate = newDate.getTime()
        endDate = newDate.getTime() + (24 * 60 * 60 * 1000)

        $.ajax({
            type: "GET",
            url: "report/data/"+startDate+"/"+endDate+"/"+ye,
            data: {},
            contentType: "application/json",
            dataType: "json",
            success: function(response) {

                data = (response['result']['time_report_time'][myDate[2]+'-'+myDate[1]+'-'+myDate[0]])
                console.log(data)
                
                
                //episodes
                episodes = '';
                listss = ['15-60','10-15','5-10','3-5','2-3'];
                console.log(listss)
                ep = 1;
                for (i = 0; i<listss.length; i++){
                    for (s=0;s<data[listss[i]].length;s++){ 
                        
                        episodes = episodes + '<tr> <td> <div class="d-flex px-2 py-1">';
                        episodes = episodes + '<div class="d-flex flex-column justify-content-center"><h6 class="mb-0 text-sm">Episode'+ep+'</h6></div></div>';
                        episodes = episodes + '</td><td><p class="text-xs font-weight-bold mb-0">'+data[listss[i]][s]['from']+' - '+data[listss[i]][s]['to']+'</p></td>';
                        episodes = episodes + '<td><p class="text-xs font-weight-bold mb-0">'+data[listss[i]][s]['diff']+'</p></td>';
                        episodes = episodes + '<td class="align-middle text-center text-sm"><span class="badge badge-sm bg-gradient-success">Online</span>';
                        episodes = episodes + '</td><td class="align-middle"><a href="javascript:;" class="text-secondary font-weight-bold text-xs" data-toggle="tooltip" data-original-title="Edit user">Add Tag</a></td>';
                        episodes = episodes + '</tr>';
                        
                        console.log(ep)
                        ep = ep + 1; 
                    
                }
                }
                console.log(episodes)
                $('#episodes').html(episodes);
                
            }
    
        });

        
    });
    var firstMotion;
    var firstShipping;
    var timeIntervalCount;
    var shippingCusCount;
    var warehouses;
    var customers;
    var last_week_count;
    var total_hours;
    var total_wrk_hrs;
    var last_shipping_active;

    var lab = []
    var lab_num = []
    for (var da = 6; da >= 0; da--) {
        var date = new Date();
        date.setDate(date.getDate() - da);

        var finalDate = ("0" + date.getDate()).slice(-2) + '-' + ("0" + (date.getMonth() + 1)).slice(-2) + '-' + date.getFullYear();
        var finalDateNum = ("0" + (date.getMonth() + 1)).slice(-2) + '/' + ("0" + date.getDate()).slice(-2);
        lab.push(finalDate)
        lab_num.push(finalDateNum)
    }

 

    $.ajax({
        type: "GET",
        url: "report/box",
        data: {},
        contentType: "application/json",
        dataType: "json",
        success: function(response) {
             
          
            $("#station_name").html(response['result']['station_name']); 
        }

    });

    $.ajax({
        type: "GET",
        url: "report",
        data: {},
        contentType: "application/json",
        dataType: "json",
        success: function(response) {
            let weeklySum = [];
            var removeLoop = 0;
           
        }

    });

 
});