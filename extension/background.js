var serverhost = 'http://127.0.0.1:8000'; 
var global_url = "";

async function getCurrentTab() {
    let queryOptions = { active: true, lastFocusedWindow: true };
    let [tab] = await chrome.tabs.query(queryOptions);
    return tab.url;
}

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        //fetch active url
        console.log(request.msg);
        if (request.msg == "fetch_url") {
            getCurrentTab().then(data => sendResponse({url:data}));
            return true;
        } else {
            //use url to request JSON
            var req = serverhost + '/score/get_score/?topic=' + request.msg; 
            fetch(req)
            .then(response => response.json())
            //send JSON back to popup.js
            .then(response => sendResponse({json:response}))
            return true;  
        }    
    }
);