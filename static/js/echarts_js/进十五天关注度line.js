
var NetizenAttention = echarts.init(document.getElementById('chart_5'))

function queryStaNetizenAttention(){
   $.ajax({
        url:'/queryStaNetizenAttention',
        type:'get',
        dataType:'json',
        data:{},
        // headers:'',
        success:function (data) {

            NetizenAttention_option = {
                grid: {
                    left: '5%',
                    right: '10%',
                    top: '20%',
                    bottom: '20%',
                    containLabel: true,
                },
                tooltip: {
                    show: true,
                    trigger: 'axis',
                },
                xAxis: [
                    {
                        type: 'category',
                        axisLine: {
                            show: true,
                            lineStyle: {
                                color: '#85C1D9',
                            },
                        },
                        axisTick: {
                            show: false,
                        },
                        axisLabel: {
                            color: '#8BC4F2',
                            margin: 6,
                        },
                        splitLine: {
                            show: false,
                        },
                        boundaryGap: ['5%', '5%'],
                        data: data.stanaDateList,
                    },
                ],
                yAxis: [
                    {
                        type: 'value',
                        axisLabel: {
                            color: '#8BC4F2',
                            margin: 6,
                        },
                        splitLine: {
                            lineStyle: {
                                color: '#355C84',
                                type: 'dashed',
                            },
                        },
                    },
                ],
                series: [
                    {
                        name: '数量',
                        type: 'line',
                        symbolSize: 6,
                        itemStyle: {
                            color: '#55EFF1',
                            borderColor: '#55EFF1',
                            borderWidth: 2,
                        },
                        data: data.attentionNumList,
                    },
                ],
            };

            NetizenAttention.setOption(NetizenAttention_option)
        },
        error:function (msg) {
            console.log(msg)
        },
    })
}

queryStaNetizenAttention()
setInterval(queryStaNetizenAttention, 1000 * 60 * 60 *12)


