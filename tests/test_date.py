from gedcom5.tag import DATE


class TestCase:

    def test_actual_date(self):
        uut = DATE(0, value='13 NOV 1969')
        assert uut.year == 1969
        assert uut.month == 11
        assert uut.day == 13
        assert uut.type == 'ACT'

    def test_actual_date_short_year(self):
        uut = DATE(0, value='13 NOV 69')
        assert uut.year == 1969
        assert uut.month == 11
        assert uut.day == 13

    def test_month_year(self):
        uut = DATE(0, value='NOV 1969')
        assert uut.year == 1969
        assert uut.month == 11
        assert uut.day == 1

    def test_month_short_year(self):
        uut = DATE(0, value='NOV 69')
        assert uut.year == 1969
        assert uut.month == 11
        assert uut.day == 1

    def test_year(self):
        uut = DATE(0, value='1969')
        assert uut.year == 1969
        assert uut.month == 1
        assert uut.day == 1

    def test_short_year(self):
        uut = DATE(0, value='69')
        assert uut.year == 1969
        assert uut.month == 1
        assert uut.day == 1

    def test_before_date(self):
        uut = DATE(0, value='BEF 13 NOV 1969')
        assert uut.year == 1969
        assert uut.month == 11
        assert uut.day == 13

    def test_after_date(self):
        uut = DATE(0, value='AFT 13 NOV 1969')
        assert uut.year == 1969
        assert uut.month == 11
        assert uut.day == 13

    def test_about_date(self):
        uut = DATE(0, value='ABT 13 NOV 1969')
        assert uut.year == 1969
        assert uut.month == 11
        assert uut.day == 13

    def test_calculated_date(self):
        uut = DATE(0, value='CAL 13 NOV 1969')
        assert uut.year == 1969
        assert uut.month == 11
        assert uut.day == 13

    def test_estimated_date(self):
        uut = DATE(0, value='EST 13 NOV 1969')
        assert uut.year == 1969
        assert uut.month == 11
        assert uut.day == 13

    def test_from_to_date(self):
        uut = DATE(0, value='FROM 13 NOV 1969 TO 14 DEC 1970')
        assert uut.year == 1969
        assert uut.month == 11
        assert uut.day == 13
        assert uut.dates['FROM'].year == 1969
        assert uut.dates['FROM'].month == 11
        assert uut.dates['FROM'].day == 13
        assert uut.dates['TO'].year == 1970
        assert uut.dates['TO'].month == 12
        assert uut.dates['TO'].day == 14

    def test_between_dates(self):
        uut = DATE(0, value='BET 13 NOV 1969 AND 14 DEC 1970')
        assert uut.year == 1969
        assert uut.month == 11
        assert uut.day == 13
        assert uut.dates['BET'].year == 1969
        assert uut.dates['BET'].month == 11
        assert uut.dates['BET'].day == 13
        assert uut.dates['AND'].year == 1970
        assert uut.dates['AND'].month == 12
        assert uut.dates['AND'].day == 14

    def test_no_date(self):
        uut = DATE(0)
        assert uut.year is None
        assert uut.month is None
        assert uut.day is None

    def test_invalid_date(self):
        uut = DATE(0, value='XXX')
        assert uut.year is None

    def test_invalid_before_date(self):
        uut = DATE(0, value='BEF XXX')
        assert uut.year is None

    def test_invalid_from_date(self):
        uut = DATE(0, value='FROM XXX TO XXX')
        assert uut.year is None

    def test_invalid_between_date(self):
        uut = DATE(0, value='BET XXX AND XXX')
        assert uut.year is None

    def test_invalid_to_date(self):
        uut = DATE(0, value='FROM 01 NOV 1969 TO XXX')
        assert uut.year == 1969

    def test_invalid_and_date(self):
        uut = DATE(0, value='FROM 01 NOV 1969 TO XXX')
        assert uut.year == 1969

    def test_invalid_from_to(self):
        uut = DATE(0, value='FROM 01 NOV 1969')
        assert uut.year is None

    def test_invalid_bet_and(self):
        uut = DATE(0, value='BET 01 NOV 1969')
        assert uut.year is None
