import {apiPrefix} from "./config";

export function getFromApi(url, callback) {
    const xhr = new XMLHttpRequest();

    xhr.open("GET", apiPrefix + url);
    xhr.onload = function () {
        let err, res;
        try {
            let response = JSON.parse(xhr.response);
            if (!response.ok) {
                err = new Error(response.error);
            } else {
                res = response.result;
            }
        } catch (e) {
            err = e;
        }

        if (err) {
            console.log(`error was occurred while getting ${apiPrefix}${url}`);
            console.log(err);
        }

        callback(err, res);
    };
    xhr.send();
}


export function postToApi(url, body, callback) {
    const xhr = new XMLHttpRequest();

    xhr.open("POST", apiPrefix + url);

    xhr.onreadystatechange = function () {
        callback(xhr.response);
    };
    xhr.send(JSON.stringify(body));
}


export function patchApi(url, body, callback) {
    const xhr = new XMLHttpRequest();

    // TODO replace POST with PATCH and set up CORP policy
    xhr.open("POST", apiPrefix + url);

    xhr.onreadystatechange = function () {
        callback(xhr.response);
    };
    console.log(JSON.stringify(body));
    xhr.send(JSON.stringify(body));
}
