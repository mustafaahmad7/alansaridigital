frappe.pages['attendancereport'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'None',
		single_column: true
	});


// set primary action button
page.set_primary_action("Refresh", () => window.location.reload());

// Fetch data from API endpoint using frappe.call
function fetchDataAndRender() {
    frappe.call({
        method: "alansaridigital.alansari_digital.page.attendancereport.attendancereport.get_details",
        callback: function (response) {
            var data = response.message;
            console.log(data);
            // Render data using frappe_render template
            $(
                frappe.render_template("attendancereport", {
                    data: data,
                })
            ).appendTo(page.body);
        },
    });
}

// Fetch data on page load
$(document).ready(function() {
    fetchDataAndRender();
    
    // Set an interval to refresh data periodically (e.g., every 5 minutes)
    setInterval(function() {
        fetchDataAndRender();
    }, 5 * 60 * 1000); // 5 minutes
});




}