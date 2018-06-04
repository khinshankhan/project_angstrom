(() => {
"use strict";

const BASE_URL = "https://theorangealliance.org/apiv2";
let key = "";

function ajaxP(obj) {
	return new Promise((resolve, reject) => {
		$.ajax(obj).done(resolve).fail(reject);
	});
}

function getAPIKey() {
	ajaxP({
		url: "/get_api_key"
	})
	.then(res => {
		key = res;
	});
}

function getEvents() {
	ajaxP({
		url: `${BASE_URL}/events`,
		headers: {
			"X-Application-Origin": "Project Angstrom",
			"X-TOA-Key": key
		},
	});
}

)();

