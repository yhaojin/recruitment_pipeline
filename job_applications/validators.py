from django.core.exceptions import ValidationError


def validate_file(file):

    if file.name[-4::] != '.pdf' and file.name[-5::] != '.docx':
        raise ValidationError("Please upload only PDF or docx files.")

    print("validated!")
    pass
