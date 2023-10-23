const get_roles_URL = "http://127.0.0.1:5100/roles";
const get_roles_skills_URL = "http://127.0.0.1:5100/rolesSkills";
const get_user_skills_URL = "http://127.0.0.1:5100/userSkills";
const get_joblistings_URL = "http://127.0.0.1:5100/joblistings";
const get_appliedJobs_URL = "http://127.0.0.1:5100/get_applied_jobs_for_user";
const get_calculatealignment_URL = "http://127.0.0.1:5100/calculateAlignment";
const apply_job_URL = "http://127.0.0.1:5100/apply_for_job";
const withdraw_application_URL = "http://127.0.0.1:5100/withdraw_application";
const get_all_applicants_URL = "http://127.0.0.1:5100/get_all_applicants";

// import components 
import Navbar from "./components/navbar.js";

const urlParams = new URLSearchParams(window.location.search);
var rights = urlParams.get("rights");


// Vue
const jobsPage = Vue.createApp({
  data() {
    return {
      staffID: "140001",
      jobListings: [],
      roles: {},
      accessRight: rights,
      activeEditJobListingID: "", 
      activeEditRoleName: "", 
      searchInput: '',
      roleSkills: {},
      skill_match_dict: {},
      userSkills: [],
      // ---------------- FOR APPLY/WITHDRAW (START) ----------------
      // appliedJobs: [],
      // applyStyle: "btn btn-primary btn-block mt-2",
      // withdrawStyle: "btn btn-secondary btn-block mt-2",
      // ---------------- FOR APPLY/WITHDRAW (END) ----------------
      // apply or withdraw errorMsg (for error modal)
      errorMsg: "",
      applicants: [],
      tempJobID: "",
      applicantsDict: {},
    };
  },

  components: {
    Navbar,
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

          // In JavaScript, you use the .then() method to work with Promises and handle the
          // asynchronous result of an operation. Promises represent the eventual completion (either success or failure)
          // of an asynchronous operation, and .then() is used to specify what should happen when the Promise is resolved (successfully completed).
          this.jobListings.forEach((jobListing) => {
            this.getCalculateAlignment(jobListing.JobList_ID).then((data) => {
              this.skill_match_dict[jobListing.JobList_ID] = {
                alignment_percentage: data.alignment_percentage,
                role_skills: data.skills_by_role,
                user_skills: this.userSkills,
              };
            });
          });

          // retrieve all the applied roles for the current user
          axios
            .get(get_appliedJobs_URL + "/" + this.staffID)
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
          var roles_list = response.data["data"]["roles"];
          const roleObject = {};

          roles_list.forEach((role) => {
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
          params: { userID: userID },
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
        const applicantAlignment = await this.getCalculateAlignment(
          jobID,
          applicantSkills
        );
        let applicantSkillsInfo = {
          applicant_skills: applicantSkills,
          alignment_percentage: applicantAlignment.alignment_percentage,
          role_skills: applicantAlignment.skills_by_role,
        };
        return applicantSkillsInfo;
      } catch (error) {
        console.error("Error in getApplicantSkills:", error);
      }
    },

    // Get the alignment percentage for the job listing and the user/applicant
    getCalculateAlignment(joblist_ID, user_Skills = null) {
      if (user_Skills === null) {
        user_Skills = this.userSkills;
      }
      const params = {
        joblist_ID: joblist_ID,
        user_Skills: user_Skills.join(","),
      };
      return axios
        .get(get_calculatealignment_URL, {
          params: params,
        })
        .then((response) => {
          return response.data.data;
        })
        .catch((error) => {
          console.log("error:", error);
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

    editCloseModals() {
      var editjobModal = bootstrap.Modal.getOrCreateInstance(
        document.getElementById("editJob")
      );
      editjobModal.hide();
      this.getAllJobListings();
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
            const data = await this.getApplicantSkills(
              joblist_ID,
              applicant.Staff_ID
            );
            return {
              staff_id: applicant.Staff_ID,
              alignment_percentage: data.alignment_percentage,
              applicant_skills: data.applicant_skills,
              role_skills: data.role_skills,
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
            this.applicantsDict[applicantData.staff_id] = {
              staff_id: applicantData.staff_id,
              alignment_percentage: applicantData.alignment_percentage,
              applicant_skills: applicantData.applicant_skills,
              role_skills: applicantData.role_skills,
            };
          });
        })
        .catch((error) => {
          // Handle errors
          console.log(error);
        });
    },

    createRestriction() {
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
    },

    createJob() {
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
            // console.log("Data sent successfully:", response.data);

            var responseCode = response.data.code;
            if (responseCode === 409) {
              var errorMessage = response.data.message;
              // console.log(errorMessage);
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
      } else {
        var errorMessageNode = document.getElementById("errorMessage");
        errorMessageNode.innerHTML = "Please select a date";
      }
    },
    
    editRestriction(jobListID, jobRoleName) {
      // --------------------- TO RESTRICT USE FROM SELECTING DATES BEFORE TODAY (START) ---------------------
      this.activeEditJobListingID = jobListID 
      this.activeEditRoleName = jobRoleName 
      var today = new Date();
      var tomorrow = new Date(today);
      tomorrow.setDate(tomorrow.getDate() + 1);
      var dd = String(tomorrow.getDate()).padStart(2, "0");
      var mm = String(tomorrow.getMonth() + 1).padStart(2, "0"); //January is 0!
      var yyyy = tomorrow.getFullYear();
      tomorrow = yyyy + "-" + mm + "-" + dd;
      document.getElementById("editClosingDate").setAttribute("min", tomorrow);
      // --------------------- TO RESTRICT USE FROM SELECTING DATES BEFORE TODAY (END) ---------------------
    },

    filterJobListings() {
      console.log(this.searchInput)
      const query = this.searchInput ? this.searchInput.toLowerCase() : '';
      console.log(query)
      if (query == '') {
        this.getAllJobListings();
      }
      else {
        this.jobListings = this.jobListings.filter((job) => {
          const jobTitle = job.Role_Name.toLowerCase();
          return jobTitle.includes(query);
        });
      }
    },
    
    editJob() {
      const listingId = this.activeEditJobListingID;
      console.log(listingId)
      const newClosingDate = document.getElementById("editClosingDate").value;
      const roleName = this.activeEditRoleName;
      if (newClosingDate) {
        axios
          .post("http://127.0.0.1:5100/editListing", {
            id: listingId,
            closingDate: newClosingDate,
            roleName: roleName 
          })
          .then((response) => {
            
            var responseCode = response.data.code;
            if (responseCode === 409 || responseCode === 404) {
              var errorMessage = response.data.message;
              var errorMessageNode = document.getElementById("editErrorMessage");
              console.log(errorMessage)
              errorMessageNode.innerHTML = errorMessage;
            } else {
              var successModal = new bootstrap.Modal(
                document.getElementById("editSuccessModal")
              );
              successModal.show();
              var errorMessageNode = document.getElementById("errorMessage");
              errorMessageNode.innerHTML = "";
            }
          })
          .catch((error) => {
            console.error("Error sending data:", error);
          });
      } else {
        var errorMessageNode = document.getElementById("errorMessage");
        errorMessageNode.innerHTML = "Please select a new date";
      }
    },
    toggleDesc(job) {
      job.showDescription = !job.showDescription;
  },
  },
    
  });

const vm = jobsPage.mount("#manageJobs");