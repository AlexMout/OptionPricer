/*
************** BY ALEX MOUTURAT ****************
*/
var two_legs_strategies = ["Call Spread","Put Spread","Strangle","Risk Reversal"];

function validate(){
    var data_isValid = true;
    //Set all help block to invisible :
    $(".help-block").hide();

    var element_to_check = [$("#spot"),$("#strike"),$("#volatility")];
    var selected_strategy = $("#strategy").val();

    //If the strategy involves 2 strikes we have to check the second strike too
    //Check if the selected strategy is in the array. If so it returns the index, if not it returns -1
    if (jQuery.inArray(selected_strategy,two_legs_strategies) != -1){
        element_to_check.push($("#strike2"));
    }

    //Check if numerical values are positive :
    for(var i = 0; i < element_to_check.length; i++)
    {
        if(element_to_check[i].val() == "" || element_to_check[i].val() <= 0){
            //element_to_check[i].parentElement.className += " has-error";
            element_to_check[i].parent().addClass("has-error");
            //document.getElementById(element_to_check[i].id + "-help").style.display = "initial";

            $('#' + element_to_check[i].attr('id') + "-help").show();
            data_isValid = false;
        }
        else{
            //if parent className contains " has-error" , delete it.
            if (element_to_check[i].parent().hasClass("has-error")){
                element_to_check[i].parent().removeClass("has-error");
            }
        }
    }

    //Check if strike 1 < strike 2 if strike 2 exists
    if (jQuery.inArray(selected_strategy,two_legs_strategies) != -1)
    {
        strike = parseFloat($("#strike").val());
        strike2 = parseFloat($("#strike2").val());
        if(strike2 <= strike)
        {
            $("#strike2").parent().addClass("has-error");
            $("#strike2-help").show();
            data_isValid = false;
        }
    }

    //Check if maturity 1 is closer than maturity 2 is Calendar Spread
    if(selected_strategy == "Calendar Spread" && ($('#maturity2_datepicker').val() == "" || $('#maturity_datepicker').datepicker("getDate") >= $('#maturity2_datepicker').datepicker("getDate")))
    {
        $('#maturity-help').show();
        $('#maturity-help').parent().addClass('has-error');
        data_isValid = false;
    }
    else
    {
        if($("#maturity-help").parent().hasClass("has-error")) $("#maturity-help").parent().removeClass("has-error");

    }

    return data_isValid;
}

function on_strategy_select(){
    var selected = $('#strategy').val();

    //Check if the selected strategy is in the array. If so it returns the index, if not it returns -1
    if (jQuery.inArray(selected,two_legs_strategies) != -1 )
    {
        $('#label-strike').html("Strike Leg 1");
        $('#strike2_div').show();
        $('#maturity2_div').hide();
    }
    else if(selected == "Calendar Spread")
    {
        $('#maturity2_div').show();
        $('#strike2_div').hide();
    }
    else
    {
        $('#label-strike').html("Strike");
        $('#strike2_div').hide();
        $('#maturity2_div').hide();
    }
}