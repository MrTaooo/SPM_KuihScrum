const form = document.querySelector("form");
const jobCreationButton = document.getElementById("jobCreationButton");

// --------------------- TO RESTRICT USE FROM SELECTING DATES BEFORE TODAY (START) ---------------------
var today = new Date();
var tomorrow = new Date(today);
tomorrow.setDate(tomorrow.getDate() + 1);
var dd = String(tomorrow.getDate()).padStart(2, "0");
var mm = String(tomorrow.getMonth() + 1).padStart(2, "0"); //January is 0!
var yyyy = tomorrow.getFullYear();

tomorrow = yyyy + "-" + mm + "-" + dd;
document.getElementById("closingDate").setAttribute("min", tomorrow);
// --------------------- TO RESTRICT USE FROM SELECTING DATES BEFORE TODAY (END) ---------------------

jobCreationButton.addEventListener("click", function (event) {
  event.preventDefault(); // Prevent the default form submission behavior

  // Get the value of the date input field
  const closingDate = document.getElementById("closingDate").value;

  // Check if a date has been selected
  if (closingDate) {

    const roleTitle = document.getElementById("roleTitle").value;

    // Send the data to the Flask backend using Axios
    axios
      .post("http://127.0.0.1:5100/createListing", {
        roleTitle: roleTitle,
        closingDate: closingDate,
      })
      .then((response) => {
        console.log("Data sent successfully:", response.data);

        var responseCode = response.data.code;
        if (responseCode === 409) {
          var errorMessage = response.data.message;
          console.log(errorMessage);
          var errorMessageNode = document.getElementById("errorMessage");
          errorMessageNode.innerHTML = errorMessage;
        } else {
          var successModal = new bootstrap.Modal(
            document.getElementById("successModal")
          );
          successModal.show();

          // do we need the 2 lines below? what is the purpose?
          var errorMessageNode = document.getElementById("errorMessage");
          errorMessageNode.innerHTML = "";
        }
      })
      .catch((error) => {
        console.error("Error sending data:", error);
      });
  }
  else {
    var errorMessageNode = document.getElementById("errorMessage");
    errorMessageNode.innerHTML = "Please select a date";
  }
});