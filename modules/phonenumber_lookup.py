import phonenumbers
from phonenumbers import carrier, geocoder, timezone


class pyPhonenumber:

    def query(PhoneNumber):
        default_region = "ID"  # DEFAULT NEGARA INDONESIA

        parsed_number = phonenumbers.parse(PhoneNumber, default_region)
   


        
        timezone1 = timezone.time_zones_for_number(parsed_number)
        timezoneF = ', '.join(timezone1)
        output_dict = {
            "Location": geocoder.description_for_number(parsed_number, "id"),
            "Region Code": phonenumbers.region_code_for_number(parsed_number),
            "Timezone": timezoneF,
            "Operator": carrier.name_for_number(parsed_number, "en"),
            "Valid number": phonenumbers.is_valid_number(parsed_number),
            "Possible number": phonenumbers.is_possible_number(parsed_number),
            "International format": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            "Mobile format": phonenumbers.format_number_for_mobile_dialing(parsed_number, default_region, with_formatting=True),
            "Original number": parsed_number.national_number,
            "E.164 format": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164),
            "Country code": parsed_number.country_code,
            "Local number": parsed_number.national_number,
        }

        number_type = phonenumbers.number_type(parsed_number)
        if number_type == phonenumbers.PhoneNumberType.MOBILE:
            output_dict["Type"] = "This is a mobile number"
        elif number_type == phonenumbers.PhoneNumberType.FIXED_LINE:
            output_dict["Type"] = "This is a fixed-line number"
        else:
            output_dict["Type"] = "This is another type of number"

        return output_dict