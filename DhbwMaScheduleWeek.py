import datetime

from bs4 import BeautifulSoup

from Ical import Event


class DhbwMaScheduleWeek:
    def __init__(self, soup: BeautifulSoup):
        self.soup = soup

    def _extract_header(self) -> BeautifulSoup:
        return self.soup.find(class_='header-txt-c')

    def extract_course_name(self) -> str:
        header = self._extract_header()
        title = header.find('h1').find('span')
        return title.text

    def extract_week_no(self) -> int:
        header = self._extract_header()
        week_no_str = header.find('span', class_='header-txt-r').text.replace('KW ', '')
        return int(week_no_str)

    def extract_week_link_param(self, link_pos: int) -> str:
        header = self._extract_header()
        link = header.find_all('a')[link_pos]
        return link['href'].split('date=')[-1]

    def extract_previous_week_param(self) -> str:
        return self.extract_week_link_param(0)

    def extract_next_week_param(self) -> str:
        return self.extract_week_link_param(1)

    def extract_events(self):
        results = []

        day_lists = self.soup.find_all('ul', attrs={'data-role' : 'listview'})

        for day in day_lists:
            day_details = day.find_all('li')
            date_incomplete_str = day_details[0].text.split(', ')[-1]
            # -> i.e. `31.08`
            day = int(date_incomplete_str.split('.')[0])
            month = int(date_incomplete_str.split('.')[-1])

            current_month = datetime.datetime.now().month
            current_year = datetime.datetime.now().year

            year = current_year
            if self.extract_week_no() == 1:
                if month == 12 and current_month == 1:
                    year = current_year - 1
                elif month == 1 and current_month > 8:
                    year = current_year + 1

            for event in day_details[1:]:
                title = event.find('div', class_='cal-title').text
                location_raw = event.find('div', class_='cal-res')
                location = location_raw.text if location_raw is not None else None
                comment_raw = event.find('div', class_='cal-text')
                comment = comment_raw.text if comment_raw is not None else None

                possible_time = event.find('div', class_='cal-time')
                if possible_time is not None:
                    times = possible_time.text.split('-')
                    times[0] = times[0].split(':')
                    times[1] = times[1].split(':')
                    start = datetime.datetime(year, month, day, int(times[0][0]), int(times[0][1]))
                    end = datetime.datetime(year, month, day, int(times[1][0]), int(times[1][1]))
                else:
                    start = datetime.datetime(year, month, day, 0, 0)
                    end = datetime.datetime(year, month, day + 1, 0, 0)

                results.append(Event(title, start, end, location, comment))

        return results
