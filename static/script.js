// Function to fetch and display records from the selected table
function fetchTableData() {
    const tableName = document.getElementById("table-select").value;

    fetch(`http://127.0.0.1:5000/get_table_data/${tableName}`)
        .then(response => {
            if (!response.ok) {
                return response.json().then(error => {
                    throw new Error(error.error || 'Error fetching data');
                });
            }
            return response.json();
        })
        .then(data => {
            console.log("Fetched data:", data);

            let resultHTML = "<table><tr>";

            if (data.length > 0) {
                Object.keys(data[0]).forEach(col => {
                    resultHTML += `<th>${col}</th>`;
                });
                resultHTML += "<th>Actions</th></tr>";

                data.forEach(row => {
                    resultHTML += "<tr>";
                    Object.entries(row).forEach(([key, val]) => {
                        resultHTML += `<td>${val}</td>`;
                    });

                    // Check if it's composite primary key (e.g., orderID + prodID)
                    const primaryKeyColumns = Object.keys(row);
                    const recordId = primaryKeyColumns.map(col => row[col]).join(",");  // Join for composite keys
                    console.log("Record ID (primary key) generated:", recordId);  // Log the recordId

                    resultHTML += `
                        <td>
                            <button onclick="showEditForm('${recordId}')">Edit</button>
                            <button class="delete-btn" onclick="deleteRecord('${recordId}')">Delete</button>
                        </td>
                    `;
                    resultHTML += "</tr>";
                });
            } else {
                resultHTML += "<tr><td colspan='5'>No data available</td></tr>";
            }
            resultHTML += "</table>";
            document.getElementById("table-result").innerHTML = resultHTML;
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            document.getElementById("table-result").innerHTML = `Error fetching data: ${error.message}`;
        });
}

// Function to delete a record
// Function to delete a record
function deleteRecord(recordId) {
    console.log("Attempting to delete record with ID:", recordId);  // Debugging line

    const confirmation = confirm("Are you sure you want to delete this record?");
    if (confirmation) {
        const tableName = document.getElementById("table-select").value;
        
        // Log table name for debugging
        console.log("Table selected for deletion:", tableName);

        fetch(`http://127.0.0.1:5000/delete_record/${tableName}/${recordId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                alert("Record deleted successfully!");
                fetchTableData();  // Refresh the data
            } else {
                alert("Error deleting record: " + result.error);
            }
        })
        .catch(error => {
            console.error('Error deleting record:', error);
            alert('Error deleting record');
        });
    }
}


// Function to show the "Edit" form
function showEditForm(recordId) {
    console.log("Record ID received:", recordId);  // Debugging line to check what ID is being passed

    if (!recordId) {
        alert("Record ID is undefined or null");
        return;
    }

    const tableName = document.getElementById("table-select").value;

    // Clear existing form fields
    document.getElementById("edit-form-fields").innerHTML = "";

    // Fetch the record data from the server
    fetch(`http://127.0.0.1:5000/get_record_data/${tableName}/${recordId}`)
        .then(response => response.json())
        .then(record => {
            if (record.error) {
                alert(record.error);
                return;
            }

            // Define form fields dynamically based on record data
            for (const [key, value] of Object.entries(record)) {
                const fieldHTML = `
                    <label for="${key}">${key}:</label>
                    <input type="text" id="${key}" name="${key}" value="${value}" required>
                    <br>
                `;
                document.getElementById("edit-form-fields").insertAdjacentHTML('beforeend', fieldHTML);
            }

            // Show the form
            document.getElementById("edit-form").style.display = "block";

            // Set up the form submission handler
            document.getElementById("edit-form-content").onsubmit = function(e) {
                e.preventDefault();

                // Gather form data
                const formData = new FormData(e.target);
                const data = {};
                formData.forEach((value, key) => {
                    data[key] = value;
                });

                // Send the updated data to the server
                fetch(`http://127.0.0.1:5000/update_record/${tableName}/${recordId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                })
                .then(response => response.json())
                .then(result => {
                    if (result.success) {
                        alert("Record updated successfully!");
                        document.getElementById("edit-form").style.display = "none";
                        fetchTableData();  // Refresh the data
                    } else {
                        alert("Error updating record: " + result.error);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error updating record');
                });
            };
        })
        .catch(error => {
            console.error('Error fetching record data:', error);
            alert('Error fetching record data');
        });
}

// Function to show the "Create" form
function showCreateForm() {
    // Clear existing fields
    document.getElementById("create-form-fields").innerHTML = "";

    const tableName = document.getElementById("table-select").value;

    // Fetch columns for the selected table
    fetch(`http://127.0.0.1:5000/get_table_data/${tableName}`)
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) {
                // Generate input fields for each column dynamically
                Object.keys(data[0]).forEach(col => {
                    const fieldHTML = `
                        <label for="${col}">${col}:</label>
                        <input type="text" id="${col}" name="${col}" required>
                        <br>
                    `;
                    document.getElementById("create-form-fields").insertAdjacentHTML('beforeend', fieldHTML);
                });

                // Show the form
                document.getElementById("create-form").style.display = "block";

                // Set up the form submission handler
                document.getElementById("create-form-content").onsubmit = function(e) {
                    e.preventDefault();

                    const formData = new FormData(e.target);
                    const data = {};
                    formData.forEach((value, key) => {
                        data[key] = value;
                    });

                    // Send the data to the server
                    fetch(`http://127.0.0.1:5000/create_record/${tableName}`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(data)
                    })
                    .then(response => response.json())
                    .then(result => {
                        if (result.success) {
                            alert("Record created successfully!");
                            document.getElementById("create-form").style.display = "none";
                            fetchTableData();  // Refresh the data
                        } else {
                            alert("Error creating record: " + result.error);
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('Error creating record');
                    });
                };
            } else {
                alert('No data found for this table.');
            }
        })
        .catch(error => {
            console.error('Error fetching table data:', error);
            alert('Error fetching table data');
        });
}
