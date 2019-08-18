from flask import Flask, request, send_file, redirect, url_for, render_template 
from werkzeug.utils import secure_filename
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

filename = ""
counter = 0
UPLOAD_FOLDER = '/home/flask_files/'
ALLOWED_EXTENSIONS = set(['xlsx'])

app = Flask(__name__,static_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["DEBUG"] = True

@app.route("/", methods=["GET", "POST"])
def login_page():
    return render_template("login.html")

@app.route("/a", methods=["GET", "POST"])
def main_page():
    return render_template("mainpage.html")

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
            return render_template("upload_success.html")
    return render_template("upload.html")

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
