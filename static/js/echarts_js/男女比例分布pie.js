
var gender = echarts.init(document.getElementById('chart_2'))

function queryStaGender(){
    $.ajax({
        url:'/queryStaGender',
        type:'get',
        dataType:'json',
        data:{},
        // headers:'',
        success:function (data) {
            console.log(data)

            var gender_option = {
                title:{
                    text:'男女比例',
                    left:'50%',
                    top:'50%',
                    textAlign:'center',
                },
                tooltip:{},  //鼠标移到上面有提示
                series: [
                    {
                        type: 'pie',
                        radius: ['40%', '70%'],
                        labelLine:{  //更改指向文字的线条的相关属性
                            show:true,
                            lineStyle:{
                                color:'white'
                            }
                        },
                        label:{      //更改文字相关属性
                            color:'white'
                        },
                        // roseType:'area',    //南丁格尔玫瑰图
                        data: [
                            {
                                name: '男生',
                                value: data.maleNum,
                                itemStyle:{
                                    color:'#6c93ff'
                                }
                            },
                            {
                                name: '女生',
                                value: data.femaleNum,
                                itemStyle:{
                                    color:'#ffbba4'
                                }
                            }
                        ]
                    }
                ]
            }

            gender.setOption(gender_option)
            // gender_option.series.data[0].value = data.maleNum
            // gender_option.series.data[1].value = data.femaleNum
            // gender.setOption(gender_option)
        },
        error: function (msg) {
            console.log(msg)
        }
    })
}
queryStaGender()
setInterval(queryStaGender, 1000*60*60)




