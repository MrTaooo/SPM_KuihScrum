const get_roles_URL = "http://localhost:5100/roles";
const get_roles_description_URL = "http://localhost:5100/rolesDescription";
const get_roles_skills_URL = "http://localhost:5100/rolesSkills";
const get_joblistings_URL = "http://localhost:5100/joblistings";

// Vue
const jobsPage = Vue.createApp({
  data() {
    return {
      jobListings: [],
      roles: [],
      userType: 0,
      accessRight: 0,
      roleDescriptions: {},
      roleSkills: {},
      // ---------------- FOR APPLY/WITHDRAW (START) ----------------
      applyBtn: true,
      applyStyle: "btn btn-primary btn-block mt-2",
      withdrawStyle: "btn btn-secondary btn-block mt-2",
      // ---------------- FOR APPLY/WITHDRAW (END) ----------------
    };
  },

  mounted() {
    console.log("-------In user mounted------");
    // retrieve all job listings
    this.getAllJobListings();
  },

  methods: {
    // this function is to get the user type, by default it will be 0, which is a normal user
    // 1 will be HR
    updateUserType() {
      if (this.accessRight == 0) {
        this.accessRight = 1;
        this.getAllJobListings();
      } else {
        this.accessRight = 0;
        this.getAllJobListings();
      }
    },

    // I created this method so that i can recall this after creating a new job listing
    getAllJobListings() {
      axios
        .get(get_joblistings_URL)
        .then((response) => {
          console.log("job listings loaded");
          console.log(response);
          this.jobListings = response.data.data.joblistings;
          var current = new Date();
          const year = current.getFullYear();
          const month = (current.getMonth() + 1).toString().padStart(2, "0"); // Add leading zero if needed
          const day = current.getDate().toString().padStart(2, "0"); // Add leading zero if needed
          const date = `${year}-${month}-${day}`;
          console.log(date);
          
          // if the user is Staff, then the job listings will be filtered to only show the job listings that are not closed
          if (this.accessRight == 0) {
            for (let i = this.jobListings.length - 1; i >= 0; i--) {
              const listing = this.jobListings[i];
              console.log(listing.Closing_date);
              if (listing.Closing_date < date) {
                this.jobListings.splice(i, 1); // Remove the item at index i
              }
            }
          }

          // these 2 methods are called to populate the roles and roleDescriptions array when the page first loads
          this.getAllRoles();
          this.getRolesDescription();
          this.getRolesSkills();
          console.log(this.jobListings);
        })
        .catch((error) => {
          console.log(error);
        });
    },

    getAllRoles() {
      // on Vue instance created, load the book list
      axios
        .get(get_roles_URL)
        .then((response) => {
          this.roles = response.data["data"]["roles"].map(
            (role) => role.Role_Name
          );
        })
        .catch((error) => {
          // Errors when calling the service; such as network error,
          // service offline, etc
          console.log(error);
        });
    },

    getRolesDescription() {
      axios
        .get(get_roles_description_URL)
        .then((response) => {
          this.roleDescriptions = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getRolesSkills() {
      axios
        .get(get_roles_skills_URL)
        .then((response) => {
          this.roleSkills = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },

    // When the user click on close for the success modal, this method will run to close the createjob modal
    closeModals() {
      var createjobModal = bootstrap.Modal.getOrCreateInstance(
        document.getElementById("createJob")
      );
      createjobModal.hide();
      this.getAllJobListings();
    },

    changeStatus(event) {
      if (this.applyBtn) {
        this.applyBtn = false;

        jobID = parseInt(event.target.getAttribute("apply-joblist-id"));
        // console.log(typeof jobID)
        staffID = parseInt(event.target.getAttribute("apply-staff-id"));
        // console.log(typeof staffID)

        // console.log("TEST (START)")
        // console.log(jobID)
        // console.log(staffID)
        // console.log("TEST (END)")

        dataToSend = {
          JobList_ID: jobID,
          Staff_ID: staffID, // Assuming you have the logged-in staff's ID accessible
        };

        // Sending a POST request to apply
        axios
          .post("http://127.0.0.1:5100/apply_for_job", dataToSend)
          .then((response) => {
            // Handle successful application, maybe show a success message
            console.log("Data sent successfully:", response.data);
          })
          .catch((error) => {
            // Handle error, maybe show an error message
            console.error("Error sending data:", error);
          });

        console.log("Applied");
      } else {
        this.applyBtn = true;

        jobID = parseInt(event.target.getAttribute("apply-joblist-id"));
        staffID = parseInt(event.target.getAttribute("apply-staff-id"));

        dataToSend = {
          JobList_ID: jobID,
          Staff_ID: staffID, // Assuming you have the logged-in staff's ID accessible
        };

        // Sending a POST request to apply
        axios
          .post("http://127.0.0.1:5100/withdraw_application", dataToSend)
          .then((response) => {
            // Handle successful application, maybe show a success message
            console.log("Data sent successfully:", response.data);
          })
          .catch((error) => {
            // Handle error, maybe show an error message
            console.error("Error sending data:", error);
          });

        console.log("Withdrawed");
      }
    },
  },
});

const vm = jobsPage.mount("#jobsPage");