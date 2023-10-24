# automated test case 7: test view applicant buttons and see if apply button backend function works [backend] (positive)
def test_apply_backend():
    HR_Manage_Start()
    applicants = get_all_applicants_name()

    # Assertion
    assert "Derek Tan" in applicants, "Derek Tan is not in the applicant list"
    
    print("===============================================================================")
    if "Derek Tan" in applicants:
        print("Result: Passed!")
        print("Remarks: Derek Tan is in the applicant list")
        print(f"Remarks: Applicant List: {applicants}")
    else:
        print("Result: Failed")
        print("Derek Tan is not in the applicant list")    
    print("End of Automated Test Case 7")
    print("===============================================================================")
