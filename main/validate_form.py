from .quote import (
    validate_text,
    validate_email,
    validate_phone,
    validate_postal_code,
    validate_selection,
    validate_number,
    validate_checkboxes
)


def validate_form(response):
    fields = dict(response.POST.items())
    full_name = validate_text(fields['FullName'], 'FullName')
    email = validate_email(fields['Email'], 'Email')
    phone = validate_phone(fields['Phone'], 'Phone')
    country = validate_text(fields['Country'], 'Country')
    province = validate_text(fields['Province/State'], 'Province/State')
    county = validate_text(fields['Township/County'], 'Township/County')
    city = validate_text(fields['City'], 'City')
    postal_code = validate_postal_code(fields['Postal/ZipCode'], 'Postal/ZipCode')
    zoning = validate_selection(fields['Zoning'], 'Zoning')
    purpose = validate_selection(fields["Building'spurpose"], "Building'spurpose")
    land = validate_selection(fields['PurchasedProperty?'], 'PurchasedProperty?')
    timeline = validate_selection(fields['Timelineuntilcompletion'], 'Timelineuntilcompletion')
    width = validate_number(fields['Widthinfeet(endwall)'], 'Widthinfeet(endwall)')
    length = validate_number(fields['Lengthinfeet(sidewall)'], 'Lengthinfeet(sidewall)')
    height = validate_number(fields['Heightinfeet(eave)'], 'Heightinfeet(eave)')
    style = validate_selection(fields['Buildingstyle'], 'Buildingstyle')
    colours = validate_selection(fields['Colours'], 'Colours')
    installation = validate_selection(fields['Doyourequireprofessionalinstallation'], 'Doyourequireprofessionalinstallation')
    roof_insul = validate_selection(fields['Roofinsulation'], 'Roofinsulation')
    wall_insul = validate_selection(fields['Wallinsulation'], 'Wallinsulation')
    gutter = validate_selection(fields['Guttersanddownspouts'], 'Guttersanddownspouts')
    walk_doors = validate_number(fields['WalkDoors(peopleaccess)'], 'WalkDoors(peopleaccess)')
    oh_doors = validate_number(fields['OverheadDoors(vehicleaccess)'], 'OverheadDoors(vehicleaccess)')
    oh_door_size = validate_number(fields['SizeofOverheadDoor'], 'SizeofOverheadDoor')
    checkbox_dict = {key: value for key, value in fields.items() if 'checkbox' in key}
    checkboxes = validate_checkboxes(checkbox_dict)

    fields = [full_name, email, phone, country, province, county, city, postal_code, zoning, purpose, land, timeline,
              width, length, height, style, colours, installation, roof_insul, wall_insul, gutter, walk_doors, oh_doors,
              oh_door_size, checkboxes]

    if errors := [x for x in fields if x['error']]:
        return {x['field']: x['error'] for x in errors}

    return False
