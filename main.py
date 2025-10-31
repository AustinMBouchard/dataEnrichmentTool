import time
import contactEnrich
import fileConvert
import auth
import companyEnrich
import jsonParser
import contactSearch
import addNewContact
import naicsMatch
from tkinter import Tk, filedialog

# Data Enrichment main file.

# - Application Function: Serves as a data enrichment tool using the Zoominfo API.
# - Process Flow:
#     1. Converts a CSV file into JSON format.
#     2. Utilizes the Zoominfo API to supplement missing contact and company information.
# - Requirements: Requires an authorized Zoominfo account and the Data Enrichment Template.
# - Output: Enriched data is saved in same directory as your input file.


def select_file():
    """
    Opens a file dialog to select a CSV file.

    Returns:
        str: The path of the selected CSV file, or None if canceled.
    """
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select the CSV file to process",
        filetypes=(("CSV Files", "*.csv"),)
    )
    root.destroy()
    return file_path if file_path else None


def main():
    """
    Runs the Data Enrichment Tool, which enriches a CSV file with additional data using the ZoomInfo API.
    The user is prompted to enter their ZoomInfo credentials, select a CSV file, and then the program performs
    contact and company enrichment using the ZoomInfo API. The program then scans for missing contacts, searches
    for contact IDs, updates missing contacts, and updates the addresses in the CSV file. Finally, the program
    converts the enriched JSON file back to CSV format and saves it to disk.
    """

    # Welcome message
    print(
        "\nWelcome to the Data Enrichment Tool!\nPlease ensure you are using the most current Data Enrichment Template to prevent errors while running this application."
    )

    username, password = auth.get_login_credentials()

    # File selection and formatting
    print("Select your file using the popup window.")
    input_csv = select_file()

    if not input_csv:
        print("No file selected. Exiting the program.")
        return

    fileConvert.count_records(input_csv)

    print(f"Converting {input_csv} to JSON")
    fileConvert.csv_to_json(input_csv)

    input_json = input_csv.rsplit(".", 1)[0] + ".json"
    print("Conversion complete.")

    jsonParser.remove_spaces(input_json)

    print("Requesting new security token...")
    jwt_token = auth.authenticate(username, password)
    last_auth_time = time.time()

    print("Beginning contact enrichment...")
    jwt_token, last_auth_time = contactEnrich.contact_enrich(
        input_json, jwt_token, last_auth_time, username, password
    )
    print("\nContact enrichment complete.\nBeginning company enrichment...")

    jwt_token, last_auth_time = companyEnrich.company_enrich(
        input_json, jwt_token, last_auth_time, username, password
    )

    print("\nCompany enrichment complete.")

    print("Scanning for missing Contacts...")
    jsonParser.updateNeedsContact(input_json)

    print("Returning Contact IDs...")
    jwt_token, last_auth_time = contactSearch.contact_search( 
        input_json, jwt_token, last_auth_time, username, password
    )

    print("Updating Missing Contacts...")
    jwt_token, last_auth_time = addNewContact.add_new_contact(
        input_json, jwt_token, last_auth_time, username, password
    )
    print("\nContact updates complete.")

    # Update the addresses in the JSON file
    print("Preparing new CSV file...")
    naicsMatch.get_sector_and_industry(input_json)
    jsonParser.update_address(input_json)

    # Convert the JSON file back to CSV format
    fileConvert.json_to_csv(input_json)
    print(
        f"Data enrichment complete. Output file: {input_json.rsplit('.', 1)[0] + ' - enhanced.csv'}"
    )


if __name__ == "__main__":
    main()
