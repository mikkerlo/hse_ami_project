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

        callback(err, res);
    };
    xhr.send();
}