import {apiPrefix} from "../config";
import Cookies from "universal-cookie";

const API_TOKEN_NAME = "X-TOKEN";

export class Api {
    constructor() {
        this.apiPrefix = apiPrefix;
    }

    static _join_urls(begin, end) {
        console.log(begin + end);
        if (begin.endsWith('/') && end.startsWith('/')) {
            return begin + end.slice(1, end.length - 1);
        }

        if (!begin.endsWith('/') && !end.startsWith('/')) {
            return begin + '/' + end;
        }

        return begin + end;
    }

    async _basicRequest(apiUrl, method, body, urlArgs) {
        let headers = new Headers();
        const cookies = new Cookies();
        let token = cookies.get('userToken');
        if (token === undefined) {
            headers.append(API_TOKEN_NAME, token);
        }

        let endpointUrl = Api._join_urls(this.apiPrefix, apiUrl);

        let url = new URL(endpointUrl);
        if (urlArgs !== undefined) {
            Object.keys(urlArgs).forEach(key => url.searchParams.append(key, urlArgs[key]));
        }

        let fetchArgs = {
            method: method,
            headers: headers,
            redirect: 'false',
        };

        if (body !== undefined && body !== {}) {
            fetchArgs['body'] = body;
        }

        return fetch(url, fetchArgs);
    }

    async get(apiUrl, urlArgs) {
        return this._basicRequest(apiUrl, 'GET', {}, urlArgs);
    }

    async post(apiUrl, body) {
        return this._basicRequest(apiUrl, 'POST', body);
    }

    async patch(apiUrl, body) {
        return this._basicRequest(apiUrl, 'PATCH', body);
    }
}

