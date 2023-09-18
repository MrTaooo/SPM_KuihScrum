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




const get_roles_URL = "http://localhost:5000/roles";
const get_joblistings_URL = "http://localhost:5100/joblistings";

// Vue
const jobsPage = Vue.createApp({
  data() {
      return {
          jobListings: [],
          roles: [],
          accessRight: 0,
      };
  },

  mounted() {
      console.log("-------In user mounted------");
      // retrieve all job listings
      axios
          .get(get_joblistings_URL)
          .then((response) => {
              console.log("job listings loaded");
              console.log(response.data[0]);
              this.jobListings = response.data["data"]["joblistings"];

          })
          .catch((error) => {
              console.log(error);
          });
    
  },

  methods: {

    getAllRoles () {
      // on Vue instance created, load the book list
      axios
          .get(get_roles_URL)
          .then((response) => {
                  console.log(response);
                  this.roles = response.data["data"]["roles"];
              })
              .catch(error => {
                  // Errors when calling the service; such as network error, 
                  // service offline, etc
                  console.log(error);

              });

  },

  },
});

const vm = jobsPage.mount("#jobsPage");
