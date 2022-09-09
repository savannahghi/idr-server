/**
* Given an element, return the element's label text.
*
* This function only works if the given element has an `id` attribute and the
* element's label has a `for` attribute whose value is the given element's
* `id`. Otherwise, an empty string will be returned.
*/
function getElementLabelText($element) {
    var element_id = $($element).attr("id");
    return $(`label[for='${element_id}']`).text().trim();
}


/**
* This is a handler called to initiate a dashboard change when links inside the
* dashboard's menu on the sidebar are clicked.
*/
function switchDashboards(event) {
    event.preventDefault();
    $selected = $(this);
    // Make the current active link(s) non-active and hide their associated
    // dashboard(s).
    $selected.parent().children().each(function() {
        $previousSelection = $(this);
        $previousSelection.removeClass("active");
        $($previousSelection.attr("href")).removeClass("active show");
    });

    // Mark the current selection as active and show it's associated dashboard
    $selected.addClass("active");
    $($(this).attr("href")).addClass("active show");

    // Hide the menu after selection
    $("#accordionSidebar.toggled #dashboards-menu").removeClass("show");
}
