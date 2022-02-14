import secrets
import string
import os


def upload_to_file(instance: "Job", file_name: str) -> str:
    """ Function which takes in a file upload instance and a proposed file name, and generates a file path.

    Scenarios:
        (1) If a pdf is uploaded, the file path generated will be: "pdf/<user_name>/<file_name>_<random_string>.pdf"
        (2) If a docx is uploaded, the file path generated will be: "docx/<user_name>/<file_name>_<random_string>.docx"

    Arguments:
        instance (UploadedFile): an instance of an UploadedFile object
        file_name (str): a string of the proposed file name. In the usage in UploadedFile model, file_name comes from
          a TextField.

    Returns:
        str (a file path that depends on the file uploaded)
    """

    fn, ext = os.path.splitext(os.path.basename(file_name))

    placeholder = instance.user.username

    if ext == ".pdf":
        return os.path.join("pdf", placeholder, f"{fn}_{generate_random_string(8)}{ext}")
    elif ext == ".docx":
        return os.path.join("docx", placeholder, f"{fn}_{generate_random_string(8)}{ext}")


def generate_random_string(n: int) -> str:
    """ Generate a random string (ascii and 0 - 9) of variable length. Can be used to encrypt file names and keys etc.

    Arguments:
        n (int): an integer that determines the random string length

    Returns:
        str, the random string that was generated

    """

    return "".join(secrets.choice(string.ascii_letters+string.digits) for __ in range(n))
