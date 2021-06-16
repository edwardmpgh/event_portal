$(document).ready(function(){
    $('#{{ widget.attrs.id }}').on('change',function(){
        if( $(this).val()==="other"){
        $("#otherType").show()
        }
        else{
        $("#otherType").hide()
        }
    });
});