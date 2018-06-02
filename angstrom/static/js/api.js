"use strict";

function ajaxP(obj) {
	return new Promise((resolve, reject) => {
		$.ajax(obj).done(resolve).fail(reject);
	});
}

function getAPIKey() {
	ajaxP({
		url: "/get_api_key",
		headers: {
			"X-Application-Origin": "Project Angstrom",
			"X-TOA-Key": ""
		},
	})
}

function getEvents() {
	
}

