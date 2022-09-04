/**
 * Created by Zelgadiss Graywords on 31.10.2016.
 */


window.onload = function () {
    document.getElementById('border_color').disabled = !document.getElementById('enable_border').checked;
    document.getElementById('logo_color').disabled = !document.getElementById('enable_logo').checked;
    var simple_url_result = document.getElementById('simple_url_result');
    simple_url_result.size = simple_url_result.value.length + 20;
    var bb_code_result = document.getElementById('bb_code_result');
    bb_code_result.size = bb_code_result.value.length + 20;
    var bb_code_with_link_result = document.getElementById('bb_code_with_link_result');
    bb_code_with_link_result.size = bb_code_with_link_result.value.length + 20;
    var html_code_result = document.getElementById('html_code_result');
    html_code_result.size = html_code_result.value.length + 20;
    var html_code_with_link_result = document.getElementById('html_code_with_link_result');
    html_code_with_link_result.size = html_code_with_link_result.value.length + 20;
};

function enable_disable(checkbox, element_id) {
    document.getElementById(element_id).disabled = !checkbox.checked;
}

