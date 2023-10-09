const get_roles_URL = "http://127.0.0.1:5100/roles";
const get_roles_skills_URL = "http://127.0.0.1:5100/rolesSkills";
const get_user_skills_URL = "http://127.0.0.1:5100/userSkills";
const get_joblistings_URL = "http://127.0.0.1:5100/joblistings";
const get_appliedJobs_URL = "http://127.0.0.1:5100/get_applied_jobs_for_user";
const get_calculatealignment_URL = "http://127.0.0.1:5100/calculateAlignment";
const apply_job_URL = "http://127.0.0.1:5100/apply_for_job";
const withdraw_application_URL = "http://127.0.0.1:5100/withdraw_application";
const get_all_applicants_URL = "http://127.0.0.1:5100/get_all_applicants";

// Vue
const jobsPage = Vue.createApp({
  data() {
    return {
      staffID: "1385970", 
      jobListings: [],
      roles: {},
      accessRight: 1,
      roleSkills: {},
      skill_match_dict: {},
      userSkills: [],
      // ---------------- FOR APPLY/WITHDRAW (START) ----------------
      appliedJobs: [],
      applyStyle: "btn btn-primary btn-block mt-2",
      withdrawStyle: "btn btn-secondary btn-block mt-2",
      // ---------------- FOR APPLY/WITHDRAW (END) ----------------
      // apply or withdraw errorMsg (for error modal)
      errorMsg: "",
      applicants: [],
      tempJobID: "",
      applicantsDict: {}
    };
  },

  mounted() {
    this.getUserSkills(this.staffID);
  },
  
  methods: {

    // this function will get all job listings for the staff and hr. Staff will only see job listings that are not closed. 
    // within this function, it also calls 2 methods to populate the roles and populate the role descriptions (vue data properties)
    // the 2 functions were not placed at mounted as the page would refresh after the hr creates a new listings wihch will activate the getAllJobListings() function
    getAllJobListings() {
      axios
        .get(get_joblistings_URL)
        .then((response) => {
          this.jobListings = response.data.data.joblistings;
          var current = new Date();
          const year = current.getFullYear();
          const month = (current.getMonth() + 1).toString().padStart(2, "0"); // Add leading zero if needed
          const day = current.getDate().toString().padStart(2, "0"); // Add leading zero if needed
          const date = `${year}-${month}-${day}`;
    
          
          // if the user is Staff, then the job listings will be filtered to only show the job listings that are not closed
          if (this.accessRight == 0) {
            for (let i = this.jobListings.length - 1; i >= 0; i--) {
              const listing = this.jobListings[i];
              // console.log(listing.Closing_date);
              if (listing.Closing_date < date) {
                this.jobListings.splice(i, 1); // Remove the item at index i
              }
            }
          }

          // In JavaScript, you use the .then() method to work with Promises and handle the 
          // asynchronous result of an operation. Promises represent the eventual completion (either success or failure) 
          // of an asynchronous operation, and .then() is used to specify what should happen when the Promise is resolved (successfully completed).
          this.jobListings.forEach((jobListing) => {
            this.getCalculateAlignment(jobListing.JobList_ID)
              .then((data) => {
                this.skill_match_dict[jobListing.JobList_ID] = {
                  "alignment_percentage": data.alignment_percentage,
                  "role_skills": data.skills_by_role,
                  "user_skills": this.userSkills
                };
              });
          });
        

          // retrieve all the applied roles for the current user
          axios
            .get(get_appliedJobs_URL+ "/" + this.staffID)
            .then((response) => {
              this.appliedJobs = response.data.data.appliedJobs;
            })
            .catch((error) => {
              console.error("Error fetching applied jobs:", error);
            });
            
          // these 2 methods are called to populate the roles and roleDescriptions array when the page first loads
          this.getAllRoles();
          this.getRolesSkills();
        })
        .catch((error) => {
          console.log(error);
        });
    },

    // this function will get all the roles and role descriptions 
    getAllRoles() {
      // on Vue instance created, load the book list
      axios
        .get(get_roles_URL)
        .then((response) => {
          roles_list = response.data["data"]["roles"]
          const roleObject = {};

          roles_list.forEach(role => {
            const role_name = role.Role_Name;
            const role_desc = role.Role_Desc;
            roleObject[role_name] = role_desc;
          });
          
          this.roles = roleObject;
        })
        .catch((error) => {
          // Errors when calling the service; such as network error,
          // service offline, etc
          console.log(error);
        });
    },
    
    // this function will get all the role and it's respective skills
    getRolesSkills() {
      axios
        .get(get_roles_skills_URL)
        .then((response) => {
          this.roleSkills = response.data.data.roles_skills[0];
        })
        .catch((error) => {
          console.log(error);
        });
    },

    // this function will get all the user's/applicant's skills
    getUserSkills(userID) {
      return axios
        .get(get_user_skills_URL, {
          params: { userID: userID }
        })
        .then((response) => {
          if (this.userSkills.length === 0) {
            this.userSkills = response.data.data.user_skills;
            this.getAllJobListings();
          } 
          return response.data.data.user_skills; // Return the skills array
        })
        .catch((error) => {
          console.log(error);
        });
    },

    async getApplicantSkills(jobID, applicantID) {
      try {
        const applicantSkills = await this.getUserSkills(applicantID);
        const applicantAlignment = await this.getCalculateAlignment(jobID, applicantSkills);
        return applicantAlignment.alignment_percentage; 
      } 
      catch (error) {
        console.error('Error in getApplicantSkills:', error);
      }
    },    
    
    // Get the alignment percentage for the job listing and the user/applicant
    getCalculateAlignment(joblist_ID, user_Skills = null) {
      if (user_Skills === null) {
        user_Skills = this.userSkills;
      }
      const params = {
        joblist_ID: joblist_ID,
        user_Skills: user_Skills.join(',')
      };
      return axios
        .get(get_calculatealignment_URL, {
          params: params
        })
        .then((response) => {
          return response.data.data;
        })
        .catch((error) => {
          console.log('error:', error);
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

    // this function will apply or withdraw the job listing for the user 
    applyOrWithdraw(event, jobID) {

      // checks if the user has applied for the job listing (appliedJobs array contains the jobListID which the user has already applied for)
      if (!this.appliedJobs.includes(jobID)) {

        // retrieves the staffID from the button attribute 
        staffID = parseInt(event.target.getAttribute("apply-staff-id"));

        // stores the data to send to the apply_job URL
        dataToSend = {
          JobList_ID: jobID,
          Staff_ID: staffID, // Assuming you have the logged-in staff's ID accessible
        };

        // Sending a POST request to apply
        axios
          .post(apply_job_URL, dataToSend)
          .then((response) => {
            // console.log("Data sent successfully:", response.data);
            if (response.data.code == "200")
            {
              // only update the button and appliedJobs list if the application is submitted successfully
              this.appliedJobs.push(jobID);
            }
            else
            {
              const errorModal = new bootstrap.Modal(document.getElementById("errorModal"));
              this.errorMsg = "Unable to apply now. Please try again later";
              errorModal.show();
            }
          })
          .catch((error) => {
            // Show the error modal for 404 errors
            const errorModal = new bootstrap.Modal(document.getElementById("errorModal"));
            this.errorMsg = "Unable to apply now. Please try again later";
            errorModal.show();
            // console.error("Error sending data:", error);
          });

        // console.log("Applied");
      } 
      // withdraw function
      else {
        const index = this.appliedJobs.indexOf(jobID);
        staffID = parseInt(event.target.getAttribute("apply-staff-id"));

        dataToSend = {
          JobList_ID: jobID,
          Staff_ID: staffID, // Assuming you have the logged-in staff's ID accessible
        };

        // Sending a POST request to withdraw
        axios
          .post(withdraw_application_URL, dataToSend)
          .then((response) => {
            if (response.data.code == "200")
            {
              if (index > -1) {
                this.appliedJobs.splice(index, 1);
              }
              // console.log("Data sent successfully:", response.data);
            }
            else
            {
              const errorModal = new bootstrap.Modal(document.getElementById("errorModal"));
              this.errorMsg = "Unable to withdraw now. Please try again later";
              errorModal.show();
            }
          })
          .catch((error) => {
            const errorModal = new bootstrap.Modal(document.getElementById("errorModal"));
            this.errorMsg = "Unable to withdraw now. Please try again later";
            errorModal.show();
            // console.error("Error sending data:", error);
          });

        console.log("Withdrawed");
      }
    },

    // this function will get all the applicants for the job listing and their respective skills and alignment percentage
    getAllApplicants(joblist_ID) {
      this.tempJobID = joblist_ID;
      axios
        .get(get_all_applicants_URL + "/" + joblist_ID)
        .then((response) => {
          this.applicants = response.data["data"]["applicants"];

          // Create an array of promises for each applicant's skills
          const promises = this.applicants.map(async (applicant) => {
            const data = await this.getApplicantSkills(joblist_ID, applicant.Staff_ID);
            return {
              Staff_ID: applicant.Staff_ID,
              alignment_percentage: data,
            };
          });
    
          // Wait for all promises to resolve; I wrote 1001 awaits for nothing
          return Promise.all(promises);
        })
        .then((applicantDataArray) => {
          // Initialize applicantsDict again for the current job applicants
          this.applicantsDict = {};
    
          // Update this.applicantsDict with the results
          applicantDataArray.forEach((applicantData) => {
            this.applicantsDict[applicantData.Staff_ID] = {
              "alignment_percentage": applicantData.alignment_percentage,
            };
          });
        })
        .catch((error) => {
          // Handle errors
          console.log(error);
        });
    }
    

  },
});

const vm = jobsPage.mount("#jobsPage");