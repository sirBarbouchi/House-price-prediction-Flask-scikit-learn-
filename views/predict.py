from flask import Flask, render_template, request, jsonify, json, Blueprint, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy  
from wtforms import SelectField, Form
from flask_wtf import FlaskForm
from flask_login import current_user
from views.forms import Form
from models import City, Municipality
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import joblib


model=pickle.load(open('model.pkl','rb'))


#sc_X = joblib.load("data_transformer.joblib") 
 
pred = Blueprint('pred', __name__, template_folder='templates')

cities0 = ['Agba',
 'Akouda',
 'Ariana Ville',
 'Aïn Zaghouan',
 'Bizerte Nord',
 'Borj Cedria',
 'Borj Louzir',
 'Boumhel',
 'Béni Khiar',
 'Carthage',
 'Centre Urbain Nord',
 'Centre Ville - Lafayette',
 'Chebba',
 'Chotrana',
 'Cité El Khadra',
 'Cité Olympique',
 'Dar Châabane El Fehri',
 'Denden',
 'Djebel Jelloud',
 'Djerba - Midoun',
 'Djerba-Houmt Souk',
 'Douar Hicher',
 'El Haouaria',
 'El Mida',
 'El Mourouj',
 'El Omrane supérieur',
 'El Ouardia',
 'Ennasr',
 'Ettadhamen',
 'Ettahrir',
 'Ezzahra',
 'Ezzouhour',
 'Fouchana',
 'Gammarth',
 'Ghazela',
 'Grombalia',
 'Hammam Chott',
 'Hammam Ghezèze',
 'Hammam Lif',
 'Hammam Sousse',
 'Hammamet',
 'Hammamet Centre',
 'Hammamet Nord',
 'Hammamet Sud',
 'Hergla',
 'Jardin De Carthage',
 "Jardins D'el Menzah",
 'Kalaâ Kebira',
 'Kalaâ Sghira',
 'Kalaât El Andalous',
 'Kantaoui',
 'Korba',
 'Kélibia',
 "L'aouina",
 'La Goulette',
 'La Marsa',
 'La Soukra',
 'Le Bardo',
 'Le Kram',
 'Les Berges Du Lac',
 "M'saken",
 'Mahdia',
 'Manar',
 'Manouba Ville',
 'Medina Jedida',
 'Menzah',
 'Menzel Temime',
 'Mnihla',
 'Mohamedia',
 'Monastir',
 'Mornag',
 'Mornaguia',
 'Mrezga',
 'Mutuelleville',
 'Médina',
 'Nabeul',
 'Oued Ellil',
 'Radès',
 'Raoued',
 'Ras Jebel',
 'Sahloul',
 'Sidi Daoud',
 'Sidi El Béchir',
 'Sousse Jawhara',
 'Sousse Médina',
 'Sousse Riadh',
 'Sousse Sidi Abdelhamid',
 'Zaouit-Ksibat Thrayett']
cities1 = ['Agba',
 'Ain Draham',
 'Akouda',
 'Ariana Ville',
 'Aïn Zaghouan',
 'Bekalta',
 'Bembla',
 'Ben Gardane',
 'Bizerte Nord',
 'Borj Cedria',
 'Borj El Amri',
 'Borj Louzir',
 'Bou Salem',
 'Bouficha',
 'Boumhel',
 'Béni Khalled',
 'Béni Khiar',
 'Carthage',
 'Centre Urbain Nord',
 'Centre Ville - Lafayette',
 'Chebba',
 'Chotrana',
 'Cité El Khadra',
 'Dar Châabane El Fehri',
 'Denden',
 'Djebel Jelloud',
 'Djedeida',
 'Djerba - Midoun',
 'Djerba-Houmt Souk',
 'Douar Hicher',
 'El Battan',
 'El Guettar',
 'El Haouaria',
 'El Kabaria',
 'El Mourouj',
 'El Omrane',
 'El Omrane supérieur',
 'El Ouardia',
 'Enfidha',
 'Ennasr',
 'Ettadhamen',
 'Ettahrir',
 'Ezzahra',
 'Ezzouhour',
 'Fouchana',
 'Gafsa Nord',
 'Gafsa Sud',
 'Gammarth',
 'Ghar El Melh',
 'Grombalia',
 'Hammam Chott',
 'Hammam Ghezèze',
 'Hammam Lif',
 'Hammam Sousse',
 'Hammamet',
 'Hammamet Centre',
 'Hammamet Nord',
 'Hammamet Sud',
 'Hergla',
 'Hraïria',
 'Jardin De Carthage',
 "Jardins D'el Menzah",
 'Jemmal',
 'Jendouba',
 'Kairouan Nord',
 'Kairouan Sud',
 'Kalaâ Kebira',
 'Kalaâ Sghira',
 'Kalaât El Andalous',
 'Kantaoui',
 'Korba',
 'Ksar Hellal',
 'Ksibet el-Médiouni',
 'Ksour Essef',
 'Kélibia',
 "L'aouina",
 'La Goulette',
 'La Marsa',
 'La Soukra',
 'Le Bardo',
 'Le Kram',
 'Les Berges Du Lac',
 "M'saken",
 'Mahdia',
 'Manar',
 'Manouba Ville',
 'Mateur',
 'Medina Jedida',
 'Menzah',
 'Menzel Bourguiba',
 'Menzel Bouzelfa',
 'Menzel Jemil',
 'Menzel Temime',
 'Mnihla',
 'Mohamedia',
 'Moknine',
 'Monastir',
 'Mornag',
 'Mornaguia',
 'Mrezga',
 'Mutuelleville',
 'Médenine Nord',
 'Médenine Sud',
 'Médina',
 'Nabeul',
 'Nasrallah',
 'Oued Ellil',
 'Ouerdanine',
 'Radès',
 'Raoued',
 'Ras Jebel',
 'Sahline',
 'Sahloul',
 'Sidi Bou Said',
 'Sidi Daoud',
 'Sidi El Béchir',
 'Sidi Hassine',
 'Sidi Thabet',
 'Soliman',
 'Sousse Jawhara',
 'Sousse Médina',
 'Sousse Riadh',
 'Sousse Sidi Abdelhamid',
 'Tabarka',
 'Tataouine Nord',
 'Tataouine Sud',
 'Tebourba',
 'Tinja',
 'Téboulba',
 'Utique',
 'Zaouit-Ksibat Thrayett',
 'Zarzis',
 'Zarzouna']
price_m1 = [[3.0, 2001.0282752929813],
 [11.0, 1583.4590601917334],
 [21.0, 2103.945814066818],
 [39.0, 2177.397335841727],
 [40.0, 1013.4458509142054],
 [61.0, 3464.285714285714],
 [68.0, 2715.7894736842104],
 [78.0, 2552.680519809534],
 [84.0, 2697.8942652329747],
 [88.0, 1775.5050505050503],
 [93.0, 1297.5851683802186],
 [109.0, 1491.300563236047],
 [117.0, 2200.0],
 [9.0, 1878.6426930806774],
 [14.0, 1946.2264150943397],
 [34.0, 1970.03367003367],
 [42.0, 1924.7902889754507],
 [44.0, 1718.1318681318685],
 [50.0, 1317.5335775335775],
 [52.0, 1321.2817833507488],
 [87.0, 1439.8974190694953],
 [94.0, 974.0939742867431],
 [97.0, 1617.2144522144522],
 [108.0, 1265.76686059039],
 [8.0, 1489.9641879081526],
 [48.0, 1173.015873015873],
 [86.0, 1316.6666666666665],
 [89.0, 3000.0],
 [91.0, 892.7521755501632],
 [110.0, 2849.0873015873017],
 [127.0, 2170.7729468599036],
 [129.0, 2684.722222222222],
 [132.0, 1260.8695652173913],
 [31.0, 800.0],
 [45.0, 1369.2307692307693],
 [46.0, 1101.3976240391335],
 [1.0, 418.1818181818182],
 [12.0, 740.7407407407408],
 [63.0, 1031.25],
 [123.0, 1132.3484848484848],
 [64.0, 1013.2434745400087],
 [65.0, 797.4296536796537],
 [105.0, 375.0],
 [20.0, 1164.3815201192251],
 [73.0, 1220.18341307815],
 [83.0, 1595.2802466350854],
 [10.0, 1380.7854137447405],
 [24.0, 2170.823989419815],
 [26.0, 2200.0],
 [29.0, 1400.0],
 [30.0, 1188.118811881188],
 [85.0, 2337.5913398339494],
 [98.0, 1824.2926949959794],
 [106.0, 1310.8641975308642],
 [126.0, 2007.703081232493],
 [7.0, 5454.545454545455],
 [27.0, 2192.5225411088695],
 [28.0, 2537.125850340136],
 [101.0, 1102.9411764705883],
 [102.0, 968.915950479314],
 [131.0, 2016.5199161425578],
 [5.0, 682.3529411764706],
 [6.0, 803.5714285714286],
 [62.0, 1592.5925925925928],
 [71.0, 1776.0141093474429],
 [72.0, 2250.0],
 [95.0, 1536.5461847389558],
 [96.0, 2222.042520855991],
 [107.0, 1600.0],
 [111.0, 1.6666666666666667],
 [128.0, 2173.913043478261],
 [15.0, 910.8698992133726],
 [16.0, 1284.6687030075188],
 [23.0, 1526.9138755980864],
 [32.0, 1230.3485162180816],
 [49.0, 1561.9622777641644],
 [51.0, 1427.8734801122835],
 [54.0, 2267.875084816535],
 [55.0, 2115.951319212189],
 [56.0, 2228.5930735930733],
 [57.0, 2199.551414768806],
 [74.0, 2270.392557295212],
 [70.0, 1690.2702702702704],
 [90.0, 1385.8823529411766],
 [92.0, 1385.2810457516339],
 [99.0, 2132.0502645502647],
 [104.0, 1676.1867442901926],
 [118.0, 1468.3023040866176],
 [2.0, 1629.5164016200604],
 [13.0, 1500.0],
 [38.0, 622.2222222222222],
 [53.0, 1448.516169446402],
 [58.0, 3153.3521303258144],
 [66.0, 1692.3304473304474],
 [67.0, 1789.8601398601397],
 [69.0, 2539.815099890531],
 [82.0, 1760.5743243243244],
 [112.0, 2475.9127214249165],
 [119.0, 1913.175853018373],
 [120.0, 2072.840786048333],
 [121.0, 1213.5381285381286],
 [122.0, 1441.6267942583731],
 [130.0, 843.121868552903],
 [124.0, 1088.4496753246754],
 [125.0, 853.2051282051282],
 [0.0, 764.7058823529412],
 [4.0, 2160.2916235558723],
 [17.0, 3119.3608039938317],
 [18.0, 3448.2758620689656],
 [19.0, 1653.6675771447785],
 [22.0, 1984.1269841269843],
 [25.0, 1369.1487589538565],
 [33.0, 1266.6666666666667],
 [35.0, 1243.9977282745058],
 [36.0, 1793.3035714285716],
 [37.0, 1102.2222222222222],
 [41.0, 1058.3333333333335],
 [43.0, 1263.4188034188032],
 [47.0, 1779.69696969697],
 [59.0, 1285.0678733031675],
 [60.0, 2641.6666666666665],
 [75.0, 2862.2784262369755],
 [76.0, 2272.7272727272725],
 [77.0, 3129.5168067226887],
 [79.0, 2169.68524251806],
 [80.0, 2709.3253968253966],
 [81.0, 2314.814814814815],
 [103.0, 1587.9407051282053],
 [100.0, 1666.6666666666667],
 [113.0, 2000.0],
 [114.0, 1524.8419150858174],
 [115.0, 1745.5555555555554],
 [116.0, 1734.6642246642248]]
price_m0 = [[2.0, 2177.485928705441],
 [6.0, 1956.4183964183965],
 [13.0, 2284.9325337331334],
 [27.0, 2568.5892468313828],
 [28.0, 930.2325581395348],
 [34.0, 1657.7665010435467],
 [46.0, 2903.9523172053296],
 [49.0, 1916.6666666666665],
 [56.0, 2433.8275973204727],
 [62.0, 2086.2107803700724],
 [65.0, 2387.6906262419807],
 [67.0, 1232.528659611993],
 [78.0, 1509.501174489208],
 [5.0, 1709.1715793358671],
 [7.0, 1950.6336320989594],
 [24.0, 1767.6495577722476],
 [30.0, 1629.8114334071288],
 [32.0, 1132.5046468401488],
 [36.0, 1563.270666875279],
 [38.0, 1294.4444444444443],
 [64.0, 1617.869766768072],
 [68.0, 1040.0],
 [70.0, 1534.920634920635],
 [77.0, 1512.549588776004],
 [4.0, 1951.654795581599],
 [79.0, 1368.0225054448656],
 [12.0, 1290.3225806451612],
 [61.0, 1145.1670682258919],
 [17.0, 1651.600592390066],
 [21.0, 1135.1362683438156],
 [63.0, 1717.6909074574328],
 [71.0, 1700.4856988667027],
 [76.0, 1075.2314814814815],
 [19.0, 1715.1651651651648],
 [20.0, 2089.9150268336316],
 [69.0, 1310.3889106583072],
 [8.0, 1075.619351408825],
 [16.0, 1835.5978260869567],
 [22.0, 1375.9398496240601],
 [23.0, 1500.0],
 [35.0, 1500.0],
 [37.0, 1898.8095238095239],
 [40.0, 2434.032258823164],
 [41.0, 2616.2190442880983],
 [42.0, 2695.653565826853],
 [43.0, 2423.745372274784],
 [52.0, 1219.9366515837105],
 [51.0, 1231.3229340319124],
 [66.0, 1500.0],
 [72.0, 2243.5195106937117],
 [75.0, 2505.7875886844267],
 [1.0, 2230.5059523809523],
 [39.0, 1634.9772834861087],
 [44.0, 2301.7857142857147],
 [47.0, 1000.0],
 [48.0, 1969.6969696969697],
 [50.0, 2093.965334741536],
 [60.0, 1000.0],
 [80.0, 2132.540373170058],
 [83.0, 1999.4467979942588],
 [84.0, 2295.959595959596],
 [85.0, 2005.9537935197654],
 [86.0, 1022.6034858387799],
 [87.0, 1500.0],
 [0.0, 1340.088996763754],
 [3.0, 2290.1785714285716],
 [9.0, 2411.098329303308],
 [10.0, 2755.9523809523807],
 [11.0, 1819.873921999064],
 [14.0, 1594.6759259259259],
 [15.0, 1589.9585921325051],
 [18.0, 941.1764705882352],
 [25.0, 1841.9753086419753],
 [26.0, 1202.0531400966183],
 [29.0, 1635.758047262472],
 [31.0, 923.0769230769231],
 [33.0, 1810.441176470588],
 [45.0, 3077.772461456672],
 [53.0, 1844.9460286609913],
 [54.0, 2601.3888888888887],
 [55.0, 2730.526028170007],
 [57.0, 2271.0597826086955],
 [58.0, 1681.950397616516],
 [59.0, 3402.377430044415],
 [74.0, 1969.1876750700283],
 [73.0, 1438.8888888888887],
 [81.0, 2551.7905773420475],
 [82.0, 1771.7640692640693]]
    

         
@pred.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'logged_in' in session:  
        if not session['logged_in'] :
            session['predict']=True
            return redirect(url_for('auth.login'))
        else:
            form = Form()
            form.municipality.choices = [(municipality.id_mun, municipality.municipality) for municipality in Municipality.query.all()]
            form.municipality.default = '1'
            if request.method == 'POST':
                municipality = Municipality.query.filter_by(municipality=form.municipality.data).first()
                cit = City.query.filter_by(city=form.city.data).first()
                city = str(cit)[6:-1]
                area = int(form.area.data)
                roomNumber = int(form.roomNumber.data)
                category = int(form.category.data)
                if(category == 1):
                    city_pos = cities0.index(city)
                    for e in price_m0:
                        if int(e[0]) == city_pos:
                            pr_m = e[1]
                else:
                    city_pos = cities1.index(city)
                    for e in price_m1:
                        if int(e[0]) == city_pos:
                            pr_m = e[1]

                int_features = [[city_pos, category, roomNumber, area, pr_m]]
                prediction = model.predict(int_features)
                

                return render_template('price.html',price=round(prediction[0], 2), city=city, category=category, room=roomNumber, area=area)
    else:
        session['predict']=True
        return redirect(url_for('auth.login'))

    return render_template('predict.html', form=form)
 
@pred.route('/city/<get_city>')
def citybymunicipality(get_city):
    city = City.query.filter_by(id_mun=get_city).all()
    cityArray = []
    for c in city:
        cityObj = {}
        cityObj['name'] = c.city
        cityArray.append(cityObj)
    return jsonify({'citymunicipality' : cityArray})
