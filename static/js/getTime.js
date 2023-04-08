function getTime(){
    $.ajax({
        url: "/time",
        timeout: 10000,
        success:function(data){
            $(".time_show").html(data)
        },
        error: function(xhr, tpye, errorThrown){

        }
    })
}
setInterval(getTime, 1000)