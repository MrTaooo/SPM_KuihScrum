const form = document.querySelector("form");
const roletitle = document.getElementById("roletitle").value;
const closingdate = document.getElementById("closingdate").value;


form.addEventListener("submit", function (event) {
  event.preventDefault(); // Prevent the default form submission behavior
  
  // Send the data to the Flask backend using Axios
  axios.post('https://127.0.0.1:5000/createlisting',  {,
    "roletitle":  roletitle,
    "closingdate" : closingdate, 
    })
    .then((response) => {
      console.log("Data sent successfully:", response.data);
    })
    .catch((error) => {
      console.error("Error sending data:", error);

    }); 
});
