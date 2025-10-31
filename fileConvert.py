import csv
import json
import os


def csv_to_json(input_csv_filename: str) -> None:
    """
    Convert a CSV file to a JSON file with specific field mappings and additional fields.
    Skips fully empty rows and uses newline='' for robust CSV parsing across platforms.

    Args:
        input_csv_filename (str): The path to the input CSV file.
    """

    header_mapping = {
        "Supplier Company": "companyName",
        "Supplier First Name": "firstName",
        "Supplier Last Name": "lastName",
        "Supplier Email": "emailAddress",
        "Supplier Phone": "phone",
        "Supplier Street": "companyStreet",
        "Supplier City": "companyCity",
        "Supplier State": "companyState",
        "Supplier Zip Code": "companyZipCode",
        "Supplier Country": "companyCountry",
        "Site Name": "siteName",
        "Site ID": "siteID",
        "Additional Contact Info": "additionalContactInfo",
    }

    new_json_values = {
        "zi_c_name": "",
        "zi_c_company_id": "",
        "jobTitle": "",
        "zi_c_company_name": "",
        "zi_c_phone": "",
        "zi_c_url": "",
        "zi_c_linkedin_url": "",
        "zi_c_naics6": "",
        "sectorTitle": "",
        "primaryIndustry": "",
        "zi_c_employees": "",
        "zi_c_street": "",
        "zi_c_city": "",
        "zi_c_state": "",
        "zi_c_zip": "",
        "zi_c_country": "",
        "zi_c_location_id": "",
        "needsContact": "",
        "newContactFound": "",
        "personId": "",
        "contactMatchCriteria": "",
        "enrichmentStatus": "Success",
        "errorMessage": "",
    }

    data = []

    # IMPORTANT: newline='' for proper csv handling (embedded newlines, mixed line endings)
    with open(input_csv_filename, "r", encoding="utf-8-sig", newline="") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            # Skip fully empty rows (all fields empty/whitespace)
            if not any((v or "").strip() for v in row.values()):
                continue

            # Map headers
            mapped_row = {}
            for key, value in row.items():
                new_key = header_mapping.get(key, key)
                mapped_row[new_key] = value

            # Add extra fields with defaults
            mapped_row.update(new_json_values)
            data.append(mapped_row)

    base_filename, _ = os.path.splitext(input_csv_filename)
    output_json_filename = base_filename + ".json"

    with open(output_json_filename, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


def json_to_csv(input_json: str) -> None:
    """
    Converts a JSON file to a CSV file with specified column mappings.

    Args:
        input_json (str): The file path of the input JSON file.
    """

    csv_mapping = {
        "companyName": "Supplier Company",
        "companyStreet": "Supplier Street",
        "companyCity": "Supplier City",
        "companyState": "Supplier State",
        "companyZipCode": "Supplier Zip Code",
        "companyCountry": "Supplier Country",
        "firstName": "Supplier First Name",
        "lastName": "Supplier Last Name",
        "emailAddress": "Supplier Email",
        "phone": "Supplier Phone",
        "siteName": "Site Name",
        "siteID": "Site ID",
        "additionalContactInfo": "Additional Contact Info",
        "zi_c_name": "Zoominfo Company Name",
        "zi_c_company_id": "Zoominfo Company ID",
        "zi_c_company_name": "Company HQ Name",
        "zi_c_phone": "Company Phone",
        "zi_c_url": "Website",
        "zi_c_linkedin_url": "Company LinkedIn URL",
        "jobTitle": "Contact Job Title",
        "zi_c_naics6": "6-digit NAICS Code",
        "sectorTitle": "Sector Title",
        "primaryIndustry": "Primary Industry",
        "zi_c_employees": "Number of Employees",
        "zi_c_street": "Company Street",
        "zi_c_city": "Company City",
        "zi_c_state": "Company State",
        "zi_c_zip": "Company Zip Code",
        "zi_c_country": "Company Country",
        "zi_c_location_id": "Company Location ID",
        "needsContact": "Needs New Contact",
        "newContactFound": "New Contact Found",
        "personId": "Contact Person ID",
        "contactMatchCriteria": "Contact Match Criteria",
        "company_match_criteria": "Company Match Criteria",
        "enrichmentStatus": "Enrichment Status",
        "errorMessage": "Error Message",
    }

    with open(input_json, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    # Build header set from actual data to avoid missing/unexpected keys
    all_keys = set()
    for entry in data:
        all_keys.update(entry.keys())

    # Preserve mapping order first...
    mapped_keys = [k for k in csv_mapping if k in all_keys]

    # ...then add any unmapped keys in the order they first appear in the JSON data
    seen = set(mapped_keys)
    unmapped_keys = []
    for entry in data:
        for key in entry.keys():
            if key not in seen:
                seen.add(key)
                unmapped_keys.append(key)

    combined_keys = mapped_keys + unmapped_keys
    headers = [csv_mapping.get(key, key) for key in combined_keys]

    base_name = os.path.splitext(input_json)[0]
    csv_file_path = f"{base_name} - Enhanced.csv"

    # newline='' for correct csv writer behavior across platforms
    with open(csv_file_path, "w", newline="", encoding="utf-8-sig") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=headers)
        csv_writer.writeheader()

        for entry in data:
            row = {csv_mapping.get(k, k): v for k, v in entry.items()}
            csv_writer.writerow(row)


def count_records(input_csv_filename: str) -> None:
    """
    Counts the number of non-empty data rows in a CSV file (skips header and fully empty rows).

    Args:
        input_csv_filename (str): The path to the input CSV file.
    """
    # newline='' for robust parsing; utf-8-sig to strip potential BOM
    with open(input_csv_filename, "r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.reader(csv_file)
        # Skip header
        next(reader, None)
        record_count = sum(1 for row in reader if any((field or "").strip() for field in row))

    print(f"\nInitialization succeeded.\nThe CSV file has {record_count} rows.\n")
