/*标准——雷达图*/
var radar = echarts.init(document.getElementById('chart_1'));

function queryHotTopicList(){
    $.ajax({
        url:'/queryHotTopicList',
        type:'get',
        dataType:'json',
        data:{},
        // headers:'',
        success:function(data){
            console.log(data)

            var radar_option = {
                title: {
                    text: ''
                },
                tooltip: {
                    position: function(point, params, dom, rect, size) {
                        //其中point为当前鼠标的位置，size中有两个属性：viewSize和contentSize，分别为外层div和tooltip提示框的大小
                        var x = point[0];//
                        var y = point[1];
                        var viewWidth = size.viewSize[0];
                        var viewHeight = size.viewSize[1];
                        var boxWidth = size.contentSize[0];
                        var boxHeight = size.contentSize[1];
                        var posX = 0;//x坐标位置
                        var posY = 0;//y坐标位置

                        if (x < boxWidth) {//左边放不开
                            posX = 5;
                        } else {//左边放的下
                            posX = x - boxWidth;
                        }

                        if (y < boxHeight) {//上边放不开
                            posY = 5;
                        } else {//上边放得下
                            posY = y - boxHeight;
                        }
                        return [posX, posY];
                    }
                },
                legend: {

                    data: ['正面倾向', '负面倾向'],
                    x:"center",
                    y:'bottom',
                    textStyle:{
                        color:"#fff"
                    }
                },
                color: [ '#f6731b', '#0cc3a5'],
                radar: {
                    name:{
                        textStyle: {
                            //设置颜色
                            color:'#fff'
                        },
                        formatter: function(value) {
                            let list = value.split("");
                            let result="";
                            for(let i=1;i<=list.length;i++) {
                                if(!(i%8)&&list[i]!=undefined) {
                                    result += list[i-1]+'\n';
                                }else {
                                    result += list[i-1];
                                }
                            }
                            return result;
                        }
                    },
                    indicator: data.indicators, // [{"name": "带of给", "max": 1},{"name": "带ofefa给", "max": 1},{"name": "eaeg给", "max": 1}],
                    center: ['50%','50%'],
                    radius: "52%"
                },
                series: [{
                    name: '',
                    type: 'radar',
                    itemStyle : {
                        normal : {
                            splitLine: {
                                lineStyle: {

                                }
                            },
                            label: {
                                show: false,
                                textStyle:{
                                },
                                formatter:function(params) {
                                    return params.value;}
                            },
                        }
                    },
                    data : [
                        {
                            value : data.positiveValues,  //[0.25, 0.45, 0.89],
                            name : '正面倾向'
                        },
                        {
                            value : data.negativeValues,  //[0.54, 0.58, 0.56],
                            name : '负面倾向'
                        }
                    ]
                }]
            };
            radar.setOption(radar_option);

            // radar_option.radar.indicator = data.indicators;
            // radar_option.series.data[0].value = data.positiveValues;
            // radar_option.series.data[1].value = data.negativeValues;
            // radar.setOption(radar_option);
        },
        error: function(msg){
            console.log(msg)
        }
    });
}
queryHotTopicList()
setInterval(queryHotTopicList, 1000*60*60)




