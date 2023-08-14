"""This is a sample Python script."""
import uuid


class UserProfile:
    """
    This is model to store data from csv
    """

    def __init__(self, _id: uuid, user_name: str, email: str, domain_name: str,
                 birthday: str, job_area: str, country: str):
        self._id: uuid = _id
        self.user_name = user_name
        self.email = email
        self.domain_name = domain_name
        self.birthday = birthday
        self.job_area = job_area
        self.country = country
