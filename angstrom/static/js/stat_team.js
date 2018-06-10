//console.log(themain);

function get_data(){
    var set = [];
    var set2 = [];
    var name = [];
    var name2 = [];
    var promises = [];
    for (var k = 0; k < maindata.length; k++){
	//console.log(maindata[k][1]);
	/* $.ajax returns a promise*/
	name.push(maindata[k][1]);
	name2.push(maindata[k][2]);
	var request = $.ajax({
            /* the ajax config*/
	    url: maindata[k][1],
	    success: function(result){
		result = JSON.parse(result);
		temp = []
		if (result != undefined && result['data'][0]['values'].length > 0){
		    result['data'][0]['values'].forEach(function(element) {
			temp.push(element[1]);
		    });
		    var sum = temp.reduce(function(a, b) { return a + b; });
		    var avg = sum / temp.length;
		    avg = Math.round(avg * 100) / 100
		    //console.log(avg);
		    //console.log(name2);
		    set.push(avg);
		    //console.log(avg);
		}else{
		    set.push(0);
		}
	    }
	})

	promises.push( request);
    }

    $.when.apply(null, promises).done(function(){
	//console.log(maindata[0][1]);
	//console.log(set);
	// Add the contents of set to div with corresponding id of name:
	//document.getElementById(element[0][0]).appendChild(makeUL(set));
	themain.forEach(function(element) {
	    //console.log(name);
	    var nom = name[0];
	    name.splice(0, 1);

	    set2 = [];
	    for (var z = 0; z < set.length; z++){
		var combined = [set[z], name2[z]];
		set2.push(combined);
	    }
	    set2.sort(sortFunction);
	    //console.log(set2);
	    //console.log(element[0][1]);
	    //console.log(nom);
	    //console.log(set);
	    var elemExists = document.getElementById(nom);
	    if(elemExists != null){
		document.getElementById(nom).appendChild(makeUL(set2));
	    }
	});
    })
};

function sortFunction(a, b) {
    if (a[0] === b[0]) {
        return 0;
    }
    else {
        return (a[0] > b[0]) ? -1 : 1;
    }
}

function makeUL(array) {
    // Create the list element:
    var list = document.createElement('ul');

    for(var i = 0; i < array.length; i++) {
        // Create the list item:
        var item = document.createElement('li');

        // Set its contents:
	var content = array[i][1] + " : "+ array[i][0];
        item.appendChild(document.createTextNode(content));

        // Add it to the list:
        list.appendChild(item);
    }

    // Finally, return the constructed list:
    return list;
}

get_data();
