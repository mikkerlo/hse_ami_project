import React from 'react';
import {apiPrefix} from "./config";
import Cookies from 'universal-cookie';

export function basicApiRequest(url, method, body, callback) {
    const xhr = new XMLHttpRequest();
    xhr.open(method, apiPrefix + url);

    const cookies = new Cookies();
    let token = cookies.get('userToken');
    if (token) {
        xhr.setRequestHeader('X-Token', token);
    }

    xhr.onreadystatechange = function () {
        // The readyState has 5 distinct states:
        // 0 - no request initialized
        // 1 - connected to server
        // 2 - request was received
        // 3 - processing
        // 4 - Done, response received
        if (xhr.readyState === 4) {
            callback(xhr);
        }
    };
    xhr.send(body);
}

export function getFromApi(url, callback) {
    basicApiRequest(url, "GET", undefined, xhr => {
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
    });
}

export function postToApi(url, body, callback) {
    basicApiRequest(url, "POST", JSON.stringify(body), xhr => {
        callback(JSON.parse(xhr.response));
    });
}

export function patchApi(url, body, callback) {
    basicApiRequest(url, "PATCH", JSON.stringify(body), xhr => {
        callback(JSON.parse(xhr.response));
    });
}

export function deleteApi(url, body, callback) {
    basicApiRequest(url, "DELETE", JSON.stringify(body), xhr => {
        callback(JSON.parse(xhr.response));
    });
}

export function withCookieAuth(Component, options) {
    return function (props, ctx) {
        return <Component
            {...props}
            {...options}
            getUserToken={
                function () {
                    const cookies = new Cookies();
                    return cookies.get('userToken');
                }
            }
        />
    }
}