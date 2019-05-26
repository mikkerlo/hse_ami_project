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