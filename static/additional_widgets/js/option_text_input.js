$(document).ready(
    function() {
    $('#{{radio_id}} .form-check-input').on('change', function(){
        console.log($(this).val());
        if( $(this).val()==="Other"){
            //$("#id_affiliation_other").toggleClass('display-on display-off');
            $("#id_affiliation_other").removeClass('display-off');
            $("#id_affiliation_other").addClass('display-on');
            console.log('toggle on');
        }
        else{
            // $("#id_affiliation_other").toggleClass('display-off display-on');
            $("#id_affiliation_other").removeClass('display-on');
            $("#id_affiliation_other").addClass('display-off');
            console.log('toggle off');
        }
    });
    }
);