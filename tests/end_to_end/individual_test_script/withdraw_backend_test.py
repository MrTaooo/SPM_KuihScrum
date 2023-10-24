# automated test case 5: test view applicant buttons and see if withdraw button backend function works [backend] (postive)
def test_withdraw_backend():
    HR_Manage_Start()

    applicant_list = Get_All_Applicants_Name()

    # Assertion
    assert "Derek Tan" not in applicant_list, "Derek Tan is in the applicant list"

    print("===============================================================================")
    if "Derek Tan" in applicant_list:
        print("Result: Failed")
        print("Remarks: Derek Tan is in the applicant list")
        print(f"Remarks: Applicant List: {applicant_list}")
    else:
        print("Result: Passed!")
        print("Remarks: Derek Tan is not in the applicant list")   
        print(f"Remarks: Applicant List: {applicant_list}") 
    print("End of Automated Test Case 5")
    print("===============================================================================")