# DhbwMaSchedule2ProperIcal

> If you want a thing done well, do it yourself.


### Disclaimer
*This software is not affiliated, associated, authorized, endorsed by, or in any way officially connected with Duale Hochschule Baden-Württemberg or any of its subsidiaries or its affiliates.*

*This software is provided "as is" and any expressed or implied warranties, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose are disclaimed. In no event shall the author or additional contributors be liable for any direct, indirect, incidental, special, exemplary, or consequential damages (including, but not limited to, procurement of substitute goods or services; loss of use, data, or profits; or business interruption).*


### Features
- Get a live-updated iCal which works completely with Outlook, Outlook Online, Google Calendar, Thunderbird, macOS Calendar, Lotus Notes and any other sane calendar application
- Optionally request an alarm from your calendar app about your first lecture at the next day so you know how you need to set your alarm clock
- Optionally request an alarm from your calendar app a few minutes before your lectures start so you don't miss them


### API
`<..>/<uid>`
- Method: HTTP-GET
- Optional parameters:
    - `addAlarmtimeAtDayBefore=<time>`: `time` is a string like `1900`, where the first two chars specify the hour adn the last two the minute of the time for which the alarm should be set
    - `addAlarmOffsetBeforeStart=<offset>`: `offset` is specified in minutes
- Examples:
    - `http://dhbw-schedule.lucavazzano.eu/6705001`
    - `http://dhbw-schedule.lucavazzano.eu/6705001?addAlarmtimeAtDayBefore=1900&addAlarmOffsetBeforeStart=5`


### Installation
The following instructions assume that you already have Apache 2 and Python 3.4 set up on your Debian-like server.

1. Install the dependencies:
    ```
    pip3 install BeautifulSoup4 Flask
    apt-get install libapache2-mod-wsgi-py3
    ```

2. Clone this repo into `/var/www`

3. Add the following to your `apache2.conf` (`#######` denotes a placeholder you need to fill):
    ```
    <VirtualHost *:80>
        ServerName #######
        ServerAlias #######
        ServerAdmin #######

        WSGIDaemonProcess DhbwMaSchedule2ProperIcal threads=17 home=/var/www/DhbwMaSchedule2ProperIcal/
        WSGIScriptAlias / /var/www/DhbwMaSchedule2ProperIcal/DhbwMaSchedule2ProperIcal.wsgi

        <Directory /var/www/DhbwMaSchedule2ProperIcal>
            WSGIProcessGroup DhbwMaSchedule2ProperIcal
            WSGIApplicationGroup %{GLOBAL}
            WSGIScriptReloading On
            Require all granted
        </Directory>
    </VirtualHost>
    ```
4. restart your apache server service

5. If you encounter problems, consider adding also the following to your `apache2.conf`:
    ```
    # use Python 3.4
    WSGIPythonPath /etc/python3.4

    # use utf-8
    AddDefaultCharset utf-8
    ```


---


### Contributing
I'm open for all forks, feedback and Pull Requests ;)


### License
This project is licensed under the terms of the *GNU General Public License v3.0*. For further information, please look [here](http://choosealicense.com/licenses/gpl-3.0/) or [here<sup>(DE)</sup>](http://www.gnu.org/licenses/gpl-3.0.de.html).
