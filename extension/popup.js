function request_json(msg_req) {
    chrome.runtime.sendMessage(
        {msg:msg_req},
        function(response) {
            result = response.json;
            if (result.success == -1) {
                document.getElementById("loader").style.display = "none";
                document.getElementById("header").style.display = "block";
                document.getElementById("wrong-url").style.display = "block";
                document.getElementById("restricted-comments").style.display = "none";
                document.getElementById("score").style.display = "none";
                document.getElementById("chart").style.display = "none";
                document.getElementById("comments").style.display = "none";
    
            } else if (result.success == 0) {
                document.getElementById("loader").style.display = "none";
                document.getElementById("header").style.display = "block";
                document.getElementById("wrong-url").style.display = "none";
                document.getElementById("restricted-comments").style.display = "block";
                document.getElementById("score").style.display = "none";
                document.getElementById("chart").style.display = "none";
                document.getElementById("comments").style.display = "none";
            } else {
                document.getElementById("loader").style.display = "none";
                document.getElementById("header").style.display = "block";
                document.getElementById("wrong-url").style.display = "none";
                document.getElementById("restricted-comments").style.display = "none";
                document.getElementById("score").style.display = "block";
                document.getElementById("chart").style.display = "block";
                document.getElementById("comments").style.display = "block";
                document.getElementById("score").innerHTML = result.score + document.getElementById("score").innerHTML;
                document.getElementById("positive_bar").style.width = result.positive_bar;
                document.getElementById("negative_bar").style.width = result.negative_bar;
                document.getElementById("comments").innerHTML = result.comment_count + document.getElementById("comments").innerHTML;
                
                if (result.percent_positive>=20) {
                    document.getElementById("positive_bar").innerHTML = result.percent_positive + document.getElementById("positive_bar").innerHTML;
                } else {
                    document.getElementById("positive_bar").innerHTML = ".";
                    document.getElementById("positive_bar").style.color = "#0bab00";
                }

                if (result.percent_negative>=20) {
                    document.getElementById("negative_bar").innerHTML = result.percent_negative + document.getElementById("negative_bar").innerHTML;
                } else {
                    document.getElementById("negative_bar").innerHTML = ".";
                    document.getElementById("negative_bar").style.color = "#ff0000";
                }

                if (result.score>3.5) {
                    document.getElementById("score").style.background = "#0bab00";
                }
                if (result.score<2.5) {
                    document.getElementById("score").style.background = "#ff0000";
                }
            }
        }    
    )
}

chrome.runtime.sendMessage(
    {msg:"fetch_url"},
    function(response) {
        var url = response.url;
        request_json(url);
    }
)