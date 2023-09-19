const get_roles_URL = "http://localhost:5100/roles";
const get_roles_description_URL = "http://localhost:5100/rolesDescription";
const get_joblistings_URL = "http://localhost:5100/joblistings";

// Vue
const jobsPage = Vue.createApp({
  data() {
      return {
          jobListings: [],
          roles: [],
          accessRight: 0,
          roleDescriptions: {}
      };
  },

  mounted() {
      console.log("-------In user mounted------");
      // retrieve all job listings
      axios
          .get(get_joblistings_URL)
          .then((response) => {
              console.log("job listings loaded");
              console.log(response);
              this.jobListings = response.data.data.joblistings;
              var current = new Date();
              const year = current.getFullYear();
              const month = (current.getMonth() + 1).toString().padStart(2, '0'); // Add leading zero if needed
              const day = current.getDate().toString().padStart(2, '0'); // Add leading zero if needed
              const date = `${year}-${month}-${day}`;
              console.log(date)
              for (let i = this.jobListings.length - 1; i >= 0; i--) {
                const listing = this.jobListings[i];
                console.log(listing.Closing_date)
                if (listing.Closing_date < date) {
                    this.jobListings.splice(i, 1); // Remove the item at index i
                }
            }
            console.log(this.jobListings);
            

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

    getRolesDescription() {
        axios
          .get(get_roles_description_URL)
          .then((response) => {
            this.rolesDescriptions = response.data;
            console.log(this.roleDescriptions)
          })
          .catch(error => {
            console.log(error);
          });
    }

  },
});

const vm = jobsPage.mount("#jobsPage");
