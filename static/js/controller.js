
function queryHotTopicList(){
    $.ajax({
        url:'/queryHotTopicList',
        type:'get',
        dataType:'json',
        data:{},
        // headers:'',
        success:function(data){
            console.log(data)

            radar_option.radar.indicator = data.indicators;
            radar_option.series.data[0].value = data.positiveValues;
            radar_option.series.data[1].value = data.negativeValues;
            radar.setOption(radar_option);
        },
        error: function(msg){
            console.log(msg)
        }
    });
}

function queryStaGender(){
    $.ajax({
        url:'/queryStaGender',
        type:'get',
        dataType:'json',
        data:{},
        // headers:'',
        success:function (data) {
            console.log(data)
            gender_option.series.data[0].value = data.maleNum
            gender_option.series.data[1].value = data.femaleNum
            gender.setOption(gender_option)
        },
        error: function (msg) {
            console.log(msg)
        }
    })
}


// queryHotTopicList()
// setInterval(queryHotTopicList, 1000)
queryStaGender()

