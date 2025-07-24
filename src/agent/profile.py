"""
Module to configurate profile sections
"""


class Education:
    def __init__(self, institution, degree_level, degree_domain, duration, location):
        self._institution = institution
        self._degree_level = degree_level
        self._degree_domain = degree_domain
        self._duration = duration
        self._location = location

    @property
    def institution(self):
        return self._institution

    @property
    def degree_level(self):
        return self._degree_level

    @property
    def degree_domain(self):
        return self._degree_domain

    @property
    def duration(self):
        return self._duration

    @property
    def location(self):
        return self._location


class Experience:
    def __init__(self, company, position, duration, description, location):
        self._company = company
        self._position = position
        self._duration = duration
        self._description = description
        self._location = location

    @property
    def company(self):
        return self._company

    @property
    def position(self):
        return self._position

    @property
    def duration(self):
        return self._duration

    @property
    def description(self):
        return self._description

    @property
    def location(self):
        return self._location


class Project:
    def __init__(self, name, duration, description, tools):
        self._name = name
        self._duration = duration
        self._description = description
        self._tools = tools

    @property
    def name(self):
        return self._name

    @property
    def duration(self):
        return self._duration

    @property
    def description(self):
        return self._description

    @property
    def tools(self):
        return self._tools


class Skill:
    def __init__(self, name, proeficiency):
        self._name = name
        self._proeficiency = proeficiency

    @property
    def name(self):
        return self._name

    @property
    def proficiency(self):
        return self._proeficiency


if __name__ == "__main__":
    exp = Experience(
        "NII",
        "SCIENTIST",
        "6 months",
        "Development of a fine-tuning architecture for LLMs",
    )

    print(exp.company)
