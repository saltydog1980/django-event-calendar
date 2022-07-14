//Setting axios defaults to handle the csrftoken and setting my base URL
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.baseURL = '/events/';

//Function to grab form fields and using axios to do a POST request to push to backside
function signUp(event) {
    event.preventDefault()
    const first_name = document.getElementById("first_name").value;
    const last_name = document.getElementById("last_name").value;
    const email = document.getElementById("email").value;
    const pw1 = document.getElementById("pswd1").value;  
    const pw2 = document.getElementById("pswd2").value; 
   //doing very basic error checking on password and alerting user if they do not match
    if(pw1 != pw2) {   
        alert("Passwords did not match"); 
    } else {
        //building my form data for Post request
        const data = new FormData();
        data.append("first_name", first_name);
        data.append("last_name", last_name);
        data.append("email", email);
        data.append("password", pw1);
        //actual post and .then
        axios.post('signup/', data).then((response) => {
            //alerting user of status and then re-directing to home page
            alert(response['data']['status']);
            window.location.href = '/events';
        });
    }
};

//log in function
function logIn(event) {
    event.preventDefault()
    //grabbing field values
    const email = document.getElementById("email").value;
    const pw1 = document.getElementById("pswd1").value;  
    //building my form data for Post request
    const data = new FormData();
    data.append("email", email);
    data.append("password", pw1);
    
    axios.post('login/', data).then((response) => {
        //alerting user of status and then re-directing to home page
        alert(response['data']['status']);
        window.location.href = '/events/';
    });

};

//function to add an item
function addItem(event) {
    event.preventDefault()
    //grabbing form values
    const name = document.getElementById("name").value;
    const description = document.getElementById("description").value;  
    const start = document.getElementById("start").value; 
    const end = document.getElementById("end").value; 
    //grabbing field values
    const data = new FormData();
    data.append("name", name);
    data.append("description", description);
    data.append("start", start);
    data.append("end", end);

    axios.post('add_item/', data).then((response) => {
        //alerting user of status and then re-directing to home page
        alert(response['data']['status']);
        window.location.href = '/events/';
    });

};

//function to update an item
function updateItem(event, id) {
    event.preventDefault()
    //grabbing form values
    const name = document.getElementById("name").value;
    const description = document.getElementById("description").value;  
    const start = document.getElementById("start").value; 
    const end = document.getElementById("end").value; 

    //building out formdata for post request
    const data = new FormData();
    data.append("id", id);
    data.append("name", name);
    data.append("description", description);
    data.append("start", start);
    data.append("end", end);
    url = `update_item/${id}/`
    
    axios.post(url, data).then((response) => {
        //alerting user and re-directing to home page
        alert(response['data']['status']);
        window.location.href = '/events/';
    });

};

//function to delete item
function deleteItem(event, id) {
    event.preventDefault()

    //building formdata for post request
    const data = new FormData();
    data.append("id", id);
    data.append("type", "delete");
    url = `update_item/${id}/`

    axios.post(url, data).then((response) => {
        //alerting user and re-firecting to home
        alert(response['data']['status']);
        window.location.href = '/events/';
    });

};