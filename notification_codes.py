from flask import Flask, request
import requests
from bs4 import BeautifulSoup

counter = 0

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=["GET", "POST"])
def adder_page():
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
                top: 60%;
                left: 50%;
                margin-right: -50%;
                transform: translate(-50%, -50%) }
        </style>
        <section class="baka1">
        <center><h4>> Сборщик нотификаций из единого реестра <</h4></center>
        <center><h1>Выбери подходящий файл:</h1></center>
        <br>
            <form action = "/uploader" method = "POST" 
                enctype = "multipart/form-data">
                <input type = "file" name = "file" />
                <input type = "submit"/>
            </form>
        <center><h4>Нажми "Отправить" и ожидай результат!</h4></center>
        </section>

        <section class="baka2">
        <center><h4>> Исправлялка технической характеристики <</h4></center>
        <center><h1>Выбери подходящий файл:</h1></center>
        <center><i><h3>эта функция в разработке</h3></i></center>
        <center><h4>Нажми "Отправить" и ожидай результат!</h4></center>
        </section>
        </body>
        </html>
    '''


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
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
        'Connection': 'keep-alive'
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


if (__name__ == "__main__"):
    app.run(host='127.0.0.1', port=5000)