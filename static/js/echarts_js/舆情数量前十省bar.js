
var TopProvinceDistribute =  echarts.init(document.getElementById('chart_6'))

function queryTopProvinceDistribute(){
   $.ajax({
        url : '/queryTopProvinceDistribute',
        type: 'get',
        dataType: 'json',
        data: {},
        success:function (data) {

            TopProvinceDistribute_option = {
                xAxis: {
                    type: 'category',
                    data: data.provinceNameList,
                    barWidth:10,
                    axisTick: {
                        show: false
                    },
                    axisLine: {
                        show: false
                    },
                    z: 10
                },
                yAxis: {
                    axisLine: {
                        show: false
                    },
                    axisTick: {
                        show: false
                    },
                    axisLabel: {
                        color: '#999'
                    }
                },
                dataZoom: [
                    {
                        type: 'inside'
                    }
                ],
                grid:{
                    bottom:'90px'
                },
                tooltip:{},  //鼠标移到上面有提示
                series: [
                    {
                        type: 'bar',
                        showBackground: false,
                        itemStyle: {
                            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                                { offset: 0, color: '#ffeaf2' },
                                { offset: 0.5, color: '#ffb4a8' },
                                { offset: 1, color: '#ff5b56' }
                            ])
                        },
                        emphasis: {
                            itemStyle: {
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                                    { offset: 0, color: '#ffeaf2' },
                                    { offset: 0.7, color: '#ffb4a8' },
                                    { offset: 1, color: '#ff5b56' }
                                ])
                            }
                        },
                        data: data.sentimentNumList
                    }
                ]
            };

            const zoomSize = 6;
            TopProvinceDistribute.on('click', function (params) {
                console.log(dataAxis[Math.max(params.dataIndex - zoomSize / 2, 0)]);
                TopProvinceDistribute.dispatchAction({
                    type: 'dataZoom',
                    startValue: dataAxis[Math.max(params.dataIndex - zoomSize / 2, 0)],
                    endValue:
                        dataAxis[Math.min(params.dataIndex + zoomSize / 2, data.length - 1)]
                });
            });

            TopProvinceDistribute.setOption(TopProvinceDistribute_option)
        },
        error:function (msg) {
            console.log(msg)
        }
    })
}

queryTopProvinceDistribute()
setInterval(queryTopProvinceDistribute, 1000 * 60 * 60)







