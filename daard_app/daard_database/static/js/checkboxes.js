function convertToSlug(Text) {
	return Text.toLowerCase().replace(/ /g, '').replace(/[^\w-]+/g, '');
}
$(document).ready(function() {

	// convert a multiple select in a multiple checkbox
	var convert_multiple_select_to_checkbox = function(selector) {
		var select_field = $(selector);

		// create table from select field
		select_field.each(function(index, item) {
			var id = $(item).attr('id'),
				name = $(item).attr('name'),
				options = $(item).children();
			var mcheckbox_table = $('<table/>', {
				id: 'mcheckbox-' + id,
				class: 'mcheckbox-table'
			}).appendTo(mcheckbox_container = $('<div/>', {
				class: 'mcheckbox-container'
			}));

			var search_row = $(`<tr class="checkbox-row search-row">
                <td class="first-check-col" colspan="2"><input class="daard_searchInput" placeholder="Type To Filter" type="text" style="width:310px; border: 2px solid #333;"></td>
                </tr>`).appendTo(mcheckbox_table);

			var old_option = ""
			options.each(function(index, option) {
				var value = $(option).attr('value'),
					label = $(option).text(),
					selected = $(option).attr('selected')
				genealogy = "is_child";
				if (!label.startsWith("---")) {
					old_option = $(option);
					prev_option_text = convertToSlug(old_option.text());
					genealogy = "is_parent"
				}
				var checkbox_row = $(`<tr class="checkbox-row ${genealogy}" data-id="${prev_option_text}">
                <td class="first-check-col"><label for="${name}'_'${value}" class="mcheckbox-label">${label}</td>
                <td class="second-check-col"><input type="checkbox" class="${prev_option_text}" id="${name}'_'${value}" name="${name}" value="${value}" ${(selected ? 'checked="checked"' : '')} /></td>
                </tr>`).appendTo(mcheckbox_table);
			})
			mcheckbox_container.insertAfter(item);
			$(item).remove();
		})
	};

	/* Apply the conversion to the desired elements (change the selector) */
	convert_multiple_select_to_checkbox("select[multiple]");

	/* Find parents with childs and remove parent checkbox */
	$('.is_parent').each(function() {
		var current_data_id = $(this).data("id");
        var table = $(this).closest('table');
		var numItems = $("tr[data-id=" + current_data_id + "]", table).length
		if (numItems >= 2) {
			$("tr[data-id=" + current_data_id + "]:eq( 0 ) td:nth-child(2) input", table).remove()
		}
	})

	/* Click logic for row */
	$('.checkbox-row td').click(function(event) {
		if (!$(event.target).is('input')) {
            event.stopPropagation();
            event.preventDefault();
			var table = $(this).closest('table');
			var current_row = $(this).closest('tr')
			var row_checkbox = $(current_row).closest('tr').find(":checkbox");
			var parent_name = $(current_row).data("id");
			var current_checkbox_state = row_checkbox.prop("checked", !row_checkbox.prop("checked"));

			$(current_row).attr('data-is-selected', ($(current_row).attr('data-is-selected') == "true" ? false : true));
			if ($(current_row).hasClass('is_parent')) {
				if ($(current_row).attr('data-is-selected') == "true") {
					$('.' + parent_name, table).prop('checked', true);
				} else {
					$('.' + parent_name, table).prop('checked', false);
				}
			}
		}
	});

    $(document).on("keyup", ".daard_searchInput", function (event) {

        //split the current value of searchInput
        var data = this.value.split(" ");
        //create a jquery object of the rows
        c_table = $(this).closest('table');
        console.log(c_table)
        var jo = $(c_table).find("tr").not('.search-row');
        if (this.value == "") {
            jo.show();
            return;
        }
        //hide all the rows
        jo.hide();

        //Recusively filter the jquery object to get results.
        jo.filter(function (i, v) {
            var $t = $(this);
            for (var d = 0; d < data.length; ++d) {
                if ($t.is(":contains('" + data[d] + "')")) {
                    return true;
                }
            }
            return false;
        })
        //show the rows that match.
        .show();
    }).focus(function () {
        this.value = "";
        $(this).css({
            "color": "black"
        });
        $(this).unbind('focus');
    }).css({
        "color": "#C0C0C0"
    });

});


$(document).ready(function() {
    // Select the textarea by its id
    var $textarea = $('#id_inventory');
    
    // Check if textarea exists
    if ($textarea.length) {
        // Parse the JSON string within the textarea
        var json = JSON.parse($textarea.val());
        
        // Stringify the JSON with indentation (4 spaces as an example)
        var formattedJson = JSON.stringify(json, null, 4);
        
        // Set the formatted JSON string back to the textarea
        $textarea.val(formattedJson);
    }


    // Select the textarea by its id
    var $textarea = $('#id_bone_relations');
    
    // Check if textarea exists
    if ($textarea.length) {
        // Parse the JSON string within the textarea
        var json = JSON.parse($textarea.val());
        
        // Stringify the JSON with indentation (4 spaces as an example)
        var formattedJson = JSON.stringify(json, null, 4);
        
        // Set the formatted JSON string back to the textarea
        $textarea.val(formattedJson);
    }
});