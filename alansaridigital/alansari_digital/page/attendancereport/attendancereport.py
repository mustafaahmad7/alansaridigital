import frappe

@frappe.whitelist()
def get_details(user=None):
    user = frappe.session.user

    query = """
        SELECT
            `tabEmployee`.`employee` AS "Employee ID",
            `tabEmployee`.`employee_name` AS "Employee Name",
            DATE(`tabEmployee Checkin`.`time`) AS "Date",
            MIN(TIME(`tabEmployee Checkin`.`time`)) AS "Check In Time",
            MAX(TIME(`tabEmployee Checkin`.`time`)) AS "Check Out Time",
            TIMEDIFF(MAX(`tabEmployee Checkin`.`time`), MIN(`tabEmployee Checkin`.`time`)) AS "Total Time",
            CASE
                WHEN MIN(TIME(`tabEmployee Checkin`.`time`)) < TIME(DATE_ADD(`tabEmployee Checkin`.`shift_start`, INTERVAL 1 HOUR)) AND 
                     MAX(TIME(`tabEmployee Checkin`.`time`)) > MIN(TIME(`tabEmployee Checkin`.`time`)) AND 
                     TIMEDIFF(MAX(`tabEmployee Checkin`.`time`), MIN(`tabEmployee Checkin`.`time`)) >= TIMEDIFF(`tabEmployee Checkin`.`shift_end`, `tabEmployee Checkin`.`shift_start`) THEN 'Present'
                ELSE 'Absent'
            END AS "Status"
        FROM
            `tabEmployee`
        LEFT JOIN
            `tabEmployee Checkin` ON `tabEmployee`.`name` = `tabEmployee Checkin`.`employee`
        WHERE
            `tabEmployee`.`status` = 'Active'
            AND DATE(`tabEmployee Checkin`.`time`) BETWEEN CURDATE() - INTERVAL 30 DAY AND CURDATE()
            {user_condition}
        GROUP BY
            `tabEmployee`.`employee`,
            `tabEmployee`.`employee_name`,
            DATE(`tabEmployee Checkin`.`time`);
    """

    if user == "Administrator":
        user_condition = ""  
    else:
        user_condition = "AND `tabEmployee`.`user_id` = %(user)s"
    
    return frappe.db.sql(query.format(user_condition=user_condition), {"user": user}, as_dict=True)