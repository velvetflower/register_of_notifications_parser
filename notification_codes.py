from flask import Flask, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

filename = ""
counter = 0
UPLOAD_FOLDER = '/home/flask_files/'
ALLOWED_EXTENSIONS = set(['xlsx'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["DEBUG"] = True

@app.route("/", methods=["GET", "POST"])
def adder_page():
    return """
    <!DOCTYPE html>
    <html lang="ru" >
    <head>

        <meta charset="UTF-8">
        <title>Таможенный помощник v0.1</title>
        <meta name="viewport" content="width=device-width, initial-scale=1"><link rel='stylesheet' href='https://fonts.googleapis.com/css?family=Open+Sans:400,800|Poppins'>
        <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/weather-icons/2.0.9/css/weather-icons.min.css'>
        <link rel="stylesheet" href="C:/Users/code971/Desktop/TEST/style.css">
        </head>
        <body>
        <style>
        body {
            font-family: "Poppins", "Open Sans", Arial, sans-serif;
            font-size: 18px;
            }

            * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            }

            .container {
            background-color: #000;
            background-size: cover;
            background-position: center;
            display: flex;
            justify-content: center;
            flex-direction: column;
            height: 100vh;
            align-items: center;
            line-height: 1;
            color: #fff;
            position: relative;
            z-index: -2;
            }
            .container:after {
            content: "";
            background: rgba(100, 100, 100, 0.4);
            position: absolute;
            left: 0;
            right: 0;
            top: 0;
            bottom: 0;
            z-index: -1;
            }
            .container #images {
            position: absolute;
            top: 0;
            bottom: 0;
            left: 0;
            right: 0;
            z-index: -1;
            overflow: hidden;
            }
            .container #images .image {
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            position: absolute;
            top: 0;
            bottom: 0;
            right: 0;
            left: 0;
            opacity: 0;
            transition: opacity 1s ease;
            }
            .container #images .image.active {
            opacity: 1;
            }
            .container #weather {
            text-transform: capitalize;
            font-family: "Open Sans", Arial, sans-serif;
            letter-spacing: 2px;
            }
            .container #bgProgress {
            height: 5px;
            width: 0;
            background: rgba(0, 0, 0, 0.4);
            position: absolute;
            top: 0;
            left: 0;
            transition: width .13s linear;
            }
            .container #clock {
            font-size: 80px;
            }
            @media screen and (max-height: 360px) {
            .container #clock {
                font-size: 64px;
            }
            }
            @media screen and (max-width: 580px) {
            .container #clock {
                font-size: 85px;
            }
            }
            @media screen and (max-width: 360px) {
            .container #clock {
                font-size: 64px;
                letter-spacing: -4px;
            }
            }
            .container #clock span {
            display: inline-block;
            font-family: "Open Sans", Arial, sans-serif;
            position: relative;
            top: -.5rem;
            line-height: .5em;
            }
            .container #date {
            padding: 0 10px;
            text-align: center;
            position: absolute;
            top: 20px;
            width: 100%;
            }
            @media screen and (max-height: 320px) {
            .container #date {
                position: static;
            }
            }
            @media screen and (max-width: 370px) {
            .container #date {
                font-size: 16px;
            }
            }

            section.baka1 {
                font-family: Arial, Geneva, Helvetica, sans-serif;
                background: rgb(20,21,24);
                color: white;
                border-radius: 2em;
                padding: 2em;
                position: absolute;
                top: 25%;
                left: 50%;
                margin-right: -50%;
                transform: translate(-50%, -50%) }
            section.baka2 {
                font-family: Arial, Geneva, Helvetica, sans-serif;
                background: rgb(20,21,24);
                color: white;
                border-radius: 2em;
                padding: 2em;
                position: absolute;
                top: 72%;
                left: 50%;
                margin-right: -50%;
                transform: translate(-50%, -50%) }

                            tml, body, div, span, applet, object, iframe,
                h1, h2, h3, h4, h5, h6, p, blockquote, pre,
                a, abbr, acronym, address, big, cite, code,
                del, dfn, em, img, ins, kbd, q, s, samp,
                small, strike, strong, sub, sup, tt, var,
                b, u, i, center,
                dl, dt, dd, ol, ul, li,
                fieldset, form, label, legend,
                table, caption, tbody, tfoot, thead, tr, th, td,
                article, aside, canvas, details, embed,
                figure, figcaption, footer, header, hgroup,
                menu, nav, output, ruby, section, summary,
                time, mark, audio, video {
                margin: 0;
                padding: 0;
                border: 0;
                font-size: 100%;
                font: inherit;
                vertical-align: baseline;
                }

                article, aside, details, figcaption, figure,
                footer, header, hgroup, menu, nav, section {
                display: block;
                }

                body {
                line-height: 1;
                }

                ol, ul {
                list-style: none;
                }

                blockquote, q {
                quotes: none;
                }

                blockquote:before, blockquote:after,
                q:before, q:after {
                content: '';
                content: none;
                }

                table {
                border-collapse: collapse;
                border-spacing: 0;
                }

                .about {
                margin: 70px auto 40px;
                padding: 8px;
                width: 260px;
                font: 10px/18px 'Lucida Grande', Arial, sans-serif;
                color: #666;
                text-align: center;
                text-shadow: 0 1px rgba(255, 255, 255, 0.25);
                background: #eee;
                background: rgba(250, 250, 250, 0.8);
                border-radius: 4px;
                background-image: -webkit-linear-gradient(top, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.1));
                background-image: -moz-linear-gradient(top, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.1));
                background-image: -o-linear-gradient(top, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.1));
                background-image: linear-gradient(to bottom, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.1));
                -webkit-box-shadow: inset 0 1px rgba(255, 255, 255, 0.3), inset 0 0 0 1px rgba(255, 255, 255, 0.1), 0 0 6px rgba(0, 0, 0, 0.2);
                box-shadow: inset 0 1px rgba(255, 255, 255, 0.3), inset 0 0 0 1px rgba(255, 255, 255, 0.1), 0 0 6px rgba(0, 0, 0, 0.2);
                }
                .about a {
                color: #333;
                text-decoration: none;
                border-radius: 2px;
                -webkit-transition: background 0.1s;
                -moz-transition: background 0.1s;
                -o-transition: background 0.1s;
                transition: background 0.1s;
                }
                .about a:hover {
                text-decoration: none;
                background: #fafafa;
                background: rgba(255, 255, 255, 0.7);
                }

                .about-links {
                height: 30px;
                }
                .about-links > a {
                float: left;
                width: 50%;
                line-height: 30px;
                font-size: 12px;
                }

                .about-author {
                margin-top: 5px;
                }
                .about-author > a {
                padding: 1px 3px;
                margin: 0 -1px;
                }

                .sign-up {
                position: relative;
                margin: 50px auto;
                width: 580px;
                padding: 33px 25px 29px;
                background: white;
                border-bottom: 1px solid #c4c4c4;
                border-radius: 5px;
                -webkit-box-shadow: 0 1px 5px rgba(0, 0, 0, 0.25);
                box-shadow: 0 1px 5px rgba(0, 0, 0, 0.25);
                }
                .sign-up:before, .sign-up:after {
                content: '';
                position: absolute;
                bottom: 1px;
                left: 0;
                right: 0;
                height: 10px;
                background: inherit;
                border-bottom: 1px solid #d2d2d2;
                border-radius: 4px;
                }
                .sign-up:after {
                bottom: 3px;
                border-color: #dcdcdc;
                }

                .sign-up-title {
                margin: -25px -25px 25px;
                padding: 15px 25px;
                line-height: 35px;
                font-size: 26px;
                font-weight: 300;
                color: #aaa;
                text-align: center;
                text-shadow: 0 1px rgba(255, 255, 255, 0.75);
                background: #f7f7f7;
                }
                .sign-up-title:before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 8px;
                background: #c4e17f;
                border-radius: 5px 5px 0 0;
                background-image: -webkit-linear-gradient(left, #c4e17f, #c4e17f 12.5%, #f7fdca 12.5%, #f7fdca 25%, #fecf71 25%, #fecf71 37.5%, #f0776c 37.5%, #f0776c 50%, #db9dbe 50%, #db9dbe 62.5%, #c49cde 62.5%, #c49cde 75%, #669ae1 75%, #669ae1 87.5%, #62c2e4 87.5%, #62c2e4);
                background-image: -moz-linear-gradient(left, #c4e17f, #c4e17f 12.5%, #f7fdca 12.5%, #f7fdca 25%, #fecf71 25%, #fecf71 37.5%, #f0776c 37.5%, #f0776c 50%, #db9dbe 50%, #db9dbe 62.5%, #c49cde 62.5%, #c49cde 75%, #669ae1 75%, #669ae1 87.5%, #62c2e4 87.5%, #62c2e4);
                background-image: -o-linear-gradient(left, #c4e17f, #c4e17f 12.5%, #f7fdca 12.5%, #f7fdca 25%, #fecf71 25%, #fecf71 37.5%, #f0776c 37.5%, #f0776c 50%, #db9dbe 50%, #db9dbe 62.5%, #c49cde 62.5%, #c49cde 75%, #669ae1 75%, #669ae1 87.5%, #62c2e4 87.5%, #62c2e4);
                background-image: linear-gradient(to right, #c4e17f, #c4e17f 12.5%, #f7fdca 12.5%, #f7fdca 25%, #fecf71 25%, #fecf71 37.5%, #f0776c 37.5%, #f0776c 50%, #db9dbe 50%, #db9dbe 62.5%, #c49cde 62.5%, #c49cde 75%, #669ae1 75%, #669ae1 87.5%, #62c2e4 87.5%, #62c2e4);
                }

                input {
                font-family: inherit;
                color: inherit;
                -webkit-box-sizing: border-box;
                -moz-box-sizing: border-box;
                box-sizing: border-box;
                }

                .sign-up-input {
                width: 100%;
                height: 50px;
                margin-bottom: 25px;
                padding: 0 15px 2px;
                font-size: 17px;
                background: white;
                border: 2px solid #ebebeb;
                border-radius: 4px;
                -webkit-box-shadow: inset 0 -2px #ebebeb;
                box-shadow: inset 0 -2px #ebebeb;
                }
                .sign-up-input:focus {
                border-color: #62c2e4;
                outline: none;
                -webkit-box-shadow: inset 0 -2px #62c2e4;
                box-shadow: inset 0 -2px #62c2e4;
                }
                .lt-ie9 .sign-up-input {
                line-height: 48px;
                }

                .sign-up-button {
                position: relative;
                vertical-align: top;
                width: 100%;
                height: 54px;
                padding: 0;
                font-size: 22px;
                color: white;
                text-align: center;
                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.25);
                background: #f0776c;
                border: 0;
                border-bottom: 2px solid #d76b60;
                border-radius: 5px;
                cursor: pointer;
                -webkit-box-shadow: inset 0 -2px #d76b60;
                box-shadow: inset 0 -2px #d76b60;
                }
                .sign-up-button:active {
                top: 1px;
                outline: none;
                -webkit-box-shadow: none;
                box-shadow: none;
                }

                :-moz-placeholder {
                color: #ccc;
                font-weight: 300;
                }

                ::-moz-placeholder {
                color: #ccc;
                opacity: 1;
                font-weight: 300;
                }

                ::-webkit-input-placeholder {
                color: #ccc;
                font-weight: 300;
                }

                :-ms-input-placeholder {
                color: #ccc;
                font-weight: 300;
                }

                ::-moz-focus-inner {
                border: 0;
                padding: 0;
                }

        </style>

        <div class="container">
        <div id="bgProgress"></div>
        <form class="sign-up">
            <h1 class="sign-up-title">Сборщик нотификаций из реестра</h1>
            <center>
            <form action = "/uploader" method = "POST" 
                enctype = "multipart/form-data">
                <input type = "file" name = "file" class="sign-up-button" />
                <input type = "submit" class="sign-up-button" />
            </form>
            </center>
        </form>
        <div id="images">
            <div class="image active" style="background-image: url('https://storage.googleapis.com/chydlx/codepen/minimalist-widget-page/dan-rogers-1156523.jpg');"></div>
            <div class="image" style="background-image: url('https://storage.googleapis.com/chydlx/codepen/minimalist-widget-page/jaanus-jagomagi-1245736.jpg');"></div>
            <div class="image" style="background-image: url('https://storage.googleapis.com/chydlx/codepen/minimalist-widget-page/patrick-tomasso-1272187.jpg');"></div>
            <div class="image" style="background-image: url('https://storage.googleapis.com/chydlx/codepen/minimalist-widget-page/sven-scheuermeier-37377.jpg');"></div>
            <div class="image" style="background-image: url('https://storage.googleapis.com/chydlx/codepen/minimalist-widget-page/tim-easley-1131834.jpg');"></div>
            <div class="image" style="background-image: url('https://storage.googleapis.com/chydlx/codepen/minimalist-widget-page/weroad-1102821.jpg');"></div>
        </div>
        <div id="date">
            <p>Monday, July 17, 2016</p>
        </div>
        <div id="clock">
            <p>
            3<span>:</span>00PM</p>
        </div>
        <div id="weather">
            <p>
            72&#8457; <i class="wi wi-day-sunny"> </i> Sunny</p>
        </div>
        <form class="sign-up">
            <h1 class="sign-up-title">Исправлялка спецификации</h1>
            <center><h1 class="sign-up-button"> <a href="/upload"> >>> Перейти к загрузке файла <<< </a> </h1></center>
        </form>
        </div>
        <!-- partial -->
        <script type="text/javascript">
            var dateObj = (function() {

            function month(num) {
                var months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"];
                return months[num];
            }

            function day(num) {
                var days = ["Воскресенье", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"];
                return days[num];
            }

            function _getDate() {
                var today = new Date(),
                date = {};

                date = {
                date: today.getDate(),
                day: day(today.getDay()), 
                month: month(today.getMonth()),
                year: today.getFullYear()
                };

                return date;
            }

            return _getDate;

            }());

            var timeObj = (function() {
            var time = {};

            function _getTime() {
                var _time = new Date(),
                hours = _time.getHours(),
                minutes = _time.getMinutes(),
                seconds = _time.getSeconds();

                time = {
                hour: hours === 0 ? hours = 12 : (hours > 12 ? hours - 12 : hours),
                mins: minutes < 10 ? "0" + minutes : minutes,
                period: hours >= 12 ? "PM" : "AM",
                secs: seconds < 10 ? "0" + seconds : seconds
                };
                
                return time;
            }

            return _getTime;
            }());

            var setDateTime = (function() {
            var elm_clock = document.querySelector('#clock p'),
                elm_date = document.querySelector('#date p');

            var defaults = {
                dateMsg: "%dateDay, %dateMonth %dateDate, %dateYear",
                timeMsg: "%timeHour<span>:</span>%timeMinutes %timePeriod"
            };

            function _setTime() {
                var msg = defaults.timeMsg
                .replace('%timeHour', timeObj().hour)
                .replace('%timeMinutes', timeObj().mins)
                .replace('%timePeriod', timeObj().period);
                elm_clock.innerHTML = msg;
            }

            function _setDate() {
                var msg = defaults.dateMsg
                .replace('%dateDay', dateObj().day)
                .replace('%dateMonth', dateObj().month)
                .replace('%dateDate', dateObj().date)
                .replace('%dateYear', dateObj().year);

                elm_date.innerHTML = msg;
            }

            _setTime();
            _setDate();

            setInterval(function() {
                _setDate();
                _setTime();
            }, 1000);
            }());

            var cycleBG = (function() {
            var progressBar = document.querySelector('#bgProgress'),
                duration = 15000,
                bgImages = document.querySelectorAll('#images .image'),
                i = 0,
                x = 0;
            
            console.log(bgImages);

            function changeBg() {
                // if i >= bgImages.length -1
                (i >= bgImages.length - 1) ? i = 0: i++;
                //change bg image
                bgImages.forEach(function(img, index){
                img.classList.remove('active');
                if(index === i) { img.classList.add('active') }
                })
            }

            changeBg();

            setInterval(function() {
                // if x === 100
                x === 100 ? (x = 0, changeBg() ) : x++;
                //progressBar width = x
                progressBar.style.width = x + '%';
            }, (duration / 100));
            }());

            var weatherWidget = (function() {
            var cont = document.querySelector('#weather');
            var apiCall = {
                id: "d65a9694ae6425d1e080326aab19db69",
                unit: "metric",
                coor: {
                lat: 45.0519047,
                lon: 38.9904714
                }
            };

            function renderWeather(data) {
                var html = "<p>";
                html += Math.floor(data.main.temp);
                html += apiCall.unit === "imperial" ? "&#8457;" : "&#8451;";
                html += " <i class='wi wi-fw wi-owm-";
                html += timeObj().period === "PM" ? "night-" : "day-";
                html += data.weather[0].id + "'></i> ";
                html += data.weather[0].description;
                html += "</p>";

                cont.innerHTML = html;
            }

            var apiURL = "https://api.openweathermap.org/data/2.5/weather?APPID=" + apiCall.id + "&units=" + apiCall.unit + "&lat=" + apiCall.coor.lat + "&lon=" + apiCall.coor.lon;

            var http = new XMLHttpRequest();

            http.onreadystatechange = function() {
                if (http.readyState == 4 && http.status == 200) {
                var data = JSON.parse(http.responseText);
                renderWeather(data);
                }
            };
            http.open("GET", apiURL, true);
            http.send();

            }());
        </script>
    </body>
</html> """

@app.route('/uploader', methods=['GET', 'POST'])
def upload_fileR():
    global counter
    if request.method == 'POST':
        counter = 0
        f = request.files['file']

        toOutput = ""
        content = f.readlines()

        used = []
        for cat in content:
            bakaCat = cat.decode("utf-8")
            nekoCat = bakaCat.replace("\n","").replace("\r","").replace(" ","")
            if nekoCat not in used:
                if nekoCat != "" and nekoCat != " " and nekoCat != None:
                    used.append(nekoCat)
                    takeAnswer = final(nekoCat)
                    toOutput += takeAnswer

        return toOutput

def final(code):
    global counter
    cookies = {
        'WSS_FullScreenMode': 'false',
    }
    headers = {
        'Origin': 'https://portal.eaeunion.org',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36 OPR/62.0.3331.117',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/xml, text/xml, */*; q=0.01',
        'Referer': 'https://portal.eaeunion.org/sites/odata/_layouts/15/Portal.EEC.Registry.Ui/DirectoryForm.aspx?ViewId=859ec98d-f4fe-423a-b6bc-d01b53fd4b7c&ListId=0e3ead06-5475-466a-a340-6f69c01b5687&ItemId=232',
        'X-CDAC-LOCALE': 'ru-ru',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }
    data = {
        'viewName': 'regui.SPLIST_TABLE_VIEW',
        'parameters': f'<p><parameter name="list" value="d84d16d7-2cc9-4cff-a13b-530f96889dbc"/><parameter name="view" value="859ec98d-f4fe-423a-b6bc-d01b53fd4b7c"/><parameter name="itemUrl" value="/sites/odata/_layouts/15/Portal.EEC.Registry.UI/DisplayForm.aspx"/><parameter name="f" value="{code}"/><parameter name="query" value="&lt;And&gt;&lt;Or&gt;&lt;Contains&gt;&lt;FieldRef Name=&quot;tmp_RegisterNotificationsCryptographicMeans_NotificationNumber&quot;/&gt;&lt;Value Type=&quot;Text&quot; &gt;&lt;![CDATA[{code}]]&gt;&lt;/Value&gt;&lt;/Contains&gt;&lt;Or&gt;&lt;Contains&gt;&lt;FieldRef Name=&quot;tmp_RegisterNotificationsCryptographicMeans_Id&quot;/&gt;&lt;Value Type=&quot;Text&quot; &gt;&lt;![CDATA[{code}]]&gt;&lt;/Value&gt;&lt;/Contains&gt;&lt;Or&gt;&lt;Contains&gt;&lt;FieldRef Name=&quot;tmp_RegisterNotificationsCryptographicMeans_Manufacturer&quot;/&gt;&lt;Value Type=&quot;Text&quot; &gt;&lt;![CDATA[{code}]]&gt;&lt;/Value&gt;&lt;/Contains&gt;&lt;Or&gt;&lt;Contains&gt;&lt;FieldRef Name=&quot;tmp_RegisterNotificationsCryptographicMeans_Name&quot;/&gt;&lt;Value Type=&quot;Text&quot; &gt;&lt;![CDATA[{code}]]&gt;&lt;/Value&gt;&lt;/Contains&gt;&lt;Or&gt;&lt;Contains&gt;&lt;FieldRef Name=&quot;tmp_RegisterNotificationsCryptographicMeans_PublicationDate&quot;/&gt;&lt;Value Type=&quot;Text&quot; &gt;&lt;![CDATA[{code}]]&gt;&lt;/Value&gt;&lt;/Contains&gt;&lt;Or&gt;&lt;Contains&gt;&lt;FieldRef Name=&quot;tmp_RegisterNotificationsCryptographicMeans_ValidityPeriod&quot;/&gt;&lt;Value Type=&quot;Text&quot; &gt;&lt;![CDATA[{code}]]&gt;&lt;/Value&gt;&lt;/Contains&gt;&lt;Or&gt;&lt;Contains&gt;&lt;FieldRef Name=&quot;tmp_RegisterNotificationsCryptographicMeans_Status&quot;/&gt;&lt;Value Type=&quot;Text&quot; &gt;&lt;![CDATA[{code}]]&gt;&lt;/Value&gt;&lt;/Contains&gt;&lt;Or&gt;&lt;Contains&gt;&lt;FieldRef Name=&quot;tmp_RegisterNotificationsCryptographicMeans_CancellationDate&quot;/&gt;&lt;Value Type=&quot;Text&quot; &gt;&lt;![CDATA[{code}]]&gt;&lt;/Value&gt;&lt;/Contains&gt;&lt;Contains&gt;&lt;FieldRef Name=&quot;tmp_RegisterNotificationsCryptographicMeans_RegistrationDate&quot;/&gt;&lt;Value Type=&quot;Text&quot; &gt;&lt;![CDATA[{code}]]&gt;&lt;/Value&gt;&lt;/Contains&gt;&lt;/Or&gt;&lt;/Or&gt;&lt;/Or&gt;&lt;/Or&gt;&lt;/Or&gt;&lt;/Or&gt;&lt;/Or&gt;&lt;/Or&gt;&lt;And&gt;&lt;Or&gt;&lt;Leq&gt;&lt;FieldRef Name=\'StartDate\'/&gt;&lt;Value Type=\'DateTime\' IncludeTimeValue=\'False\'&gt;2019-08-13T12:38:17.674Z&lt;/Value&gt;&lt;/Leq&gt;&lt;IsNull&gt;&lt;FieldRef Name=\'StartDate\'/&gt;&lt;/IsNull&gt;&lt;/Or&gt;&lt;Or&gt;&lt;Geq&gt;&lt;FieldRef Name=\'EndDate\'/&gt;&lt;Value Type=\'DateTime\' IncludeTimeValue=\'False\'&gt;2019-08-13T12:38:17.674Z&lt;/Value&gt;&lt;/Geq&gt;&lt;IsNull&gt;&lt;FieldRef Name=\'EndDate\'/&gt;&lt;/IsNull&gt;&lt;/Or&gt;&lt;/And&gt;&lt;/And&gt;"/><parameter name="filter" value=""/></p>'
    }

    response = requests.post('https://portal.eaeunion.org/sites/odata/_layouts/CDAC.Web/XmlSourceBrockerService.asmx/getViewXmlContentFriendly',
                             headers=headers, cookies=cookies, data=data)
    plain_text = response.text

    soup = BeautifulSoup(plain_text, 'lxml')

    tbl = soup.findAll('tbody')

    for tr in tbl[0].findAll('tr'):
        abusedLink = tr.get("data-href")

    normalLink = "https://portal.eaeunion.org" + abusedLink

    response = requests.post(normalLink,
                             headers=headers, cookies=cookies, data=data)

    plain_text = response.text
    soup = BeautifulSoup(plain_text, features='lxml')

    listos = []

    for items in soup.findAll("div", {"class": "cr-field-row"}):
        for baka in soup.findAll("div", {"class": "cr-field-value"}):
            heyho = baka.text.replace("\n", "").replace(
                "\r", "".replace("\xa0", ""))
            if heyho != "" and heyho != " " and heyho != None:
                listos.append(heyho)
        break
    counter += 1
    nomer = listos[0].replace(" ", "")
    ident = listos[2].replace(" ", "")
    naime = listos[5].replace("\n", "").replace("\r", "")
    izgot = listos[6].replace("\n", "").replace("\r", "")
    srokd = listos[7].replace(" ", "")
    statu = listos[8].replace(" ", "")
    regst = listos[9].replace(" ", "")
    return f"""
    <html>
        <body>
            <p>№ {counter} |=====================================><a href="/"> На главную страницу <<<</a></p>
            <p>1. Номер нотификации: {nomer}</p>
            <p>2. Идентификатор: {ident}</p>
            <p>3. Наименование товара: {naime}</p>
            <p>4. Изготовитель товара: {izgot}</p>
            <p>5. Срок действия: {srokd}</p>
            <p>6. Статус: {statu}</p>
            <p>8. Дата регистрации нотификации: {regst}</p>
        </body>
    </html>"""

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    global filename
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return '''
        <html>
        <body>
        <style>
            body {
                background: white;
                height: 100%;
                background-size: cover;
                background-repeat: no-repeat;
                background-position: center center;
                background-image: url("https://www.downloadwallpapers.info/dl/1920x1080//2014/08/16/445942_background-nature-pleasant-scenery_1920x1200_h.jpg") }
            section.uploadBaka {
                font-family: Arial, Geneva, Helvetica, sans-serif;
                background: rgb(20,21,24);
                color: white;
                border-radius: 4em;
                padding: 3em;
                position: absolute;
                top: 30%;
                left: 50%;
                margin-right: -50%;
                transform: translate(-50%, -50%) }
        </style>
        <section class="uploadBaka">
            <center><h1>2. Файл готов! Скачать?</h1></center>
            <center>
            <form action="/download">
                <input type="submit" value="Скачать!" />
            </form>
            </center>
            <a href="/" style="color:yellow;"><h3>Нажми сюда что бы вернуться на главную</h3></a>
        </section>
        </body>
        </html>
    '''

    return '''
        <html>
        <body>
        <style>
            body {
                background: white;
                height: 100%;
                background-size: cover;
                background-repeat: no-repeat;
                background-position: center center;
                background-image: url("https://www.downloadwallpapers.info/dl/1920x1080//2014/08/16/445942_background-nature-pleasant-scenery_1920x1200_h.jpg") }
            section.uploadBaka {
                font-family: Arial, Geneva, Helvetica, sans-serif;
                background: rgb(20,21,24);
                color: white;
                border-radius: 4em;
                padding: 3em;
                position: absolute;
                top: 30%;
                left: 50%;
                margin-right: -50%;
                transform: translate(-50%, -50%) }
        </style>
        <section class="uploadBaka">
            <h1>1. Выбери загружаемый файл:</h1>
            <form action="" method=post enctype=multipart/form-data>
            <p><input type=file name=file>
                <input type=submit value=Загрузить>
            </form>
        </section>
        </body>
        </html>
    '''

@app.route('/download')
def downloadFile ():
    global filename
    df = pd.read_excel(UPLOAD_FOLDER + filename).sort_values('Страна происхождения')
    empty_row = pd.DataFrame({'a':['']})
    out = UPLOAD_FOLDER + r'result.xlsx'
    writer = pd.ExcelWriter(out)
    count = 0
    for k,g in df.groupby(df['Техническая характеристика'].str.extract(r'(\w+)\s+', expand=False)):
        g.to_excel(writer, index=False, header=(count==0), startrow=count+(count!=0))
        count += len(g)
        empty_row.to_excel(writer, header=None, index=False, startrow=count+1)
        count +=1
    writer.save()
    return send_file(out, as_attachment=True)

if (__name__ == "__main__"):
    app.run(host='127.0.0.1', port=5000)