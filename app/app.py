from flask import Flask, render_template, request, url_for, redirect, session
import numpy as np
import pickle

app = Flask(__name__)
app.secret_key = "ratingKey"
@app.route('/', methods=['GET', 'POST'])
def home_page():
    request_type_str = request.method
    if request_type_str == 'GET':
        return render_template('index.html')
    else:
        values=[]
        values = [0 for i in range(32)] 
        values[0]= request.form.get("console")
        values[1]= request.form.get("alcoholReference")
        values[2]= request.form.get("animatedBlood")
        values[3]= request.form.get("Blood")
        values[4]= request.form.get("bloodAndGore")
        values[5]= request.form.get("cartoonViolence")
        values[6]= request.form.get("crudehumor")
        values[7]= request.form.get("drugReference")
        values[8]= request.form.get("fantasyViolence")
        values[9]= request.form.get("intenseViolence")
        values[10]= request.form.get("language")
        values[11]= request.form.get("lyrics")
        values[12]= request.form.get("matureHumor")
        values[13]= request.form.get("mildBlood")
        values[14]= request.form.get("mildCartoonViolence")
        values[15]= request.form.get("mildFantasyViolence")
        values[16]= request.form.get("mildLanguage")
        values[17]= request.form.get("mildLyrics")
        values[18]= request.form.get("mildSuggestiveThemes")
        values[19]= request.form.get("mildViolence")
        values[20]= request.form.get("noDescriptors")
        values[21]= request.form.get("nudity")
        values[22]= request.form.get("partialNudity")
        values[23]= request.form.get("sexualContent")
        values[24]= request.form.get("sexualThemes")
        values[25]= request.form.get("simulatedGambling")
        values[26]= request.form.get("strongLanguage")
        values[27]= request.form.get("strongSexualContent")
        values[28]= request.form.get("suggestiveThemes")
        values[29]= request.form.get("useOfAlcohol")
        values[30]= request.form.get("useOfDrugsAndAlcohol")
        values[31]= request.form.get("Violence")
        
        for i in range(32):
            if str(values[i]) == str("None"):
                values[i] = 0
            else:
                values[i] = 1

        import os
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        my_file= os.path.join(THIS_FOLDER, "random_forest_classifier_model.pkl")
        pickle_in = open(my_file, "rb")
        model = pickle.load(pickle_in)

        test_np_input = np.array([values[0],values[1],values[2],values[3],values[4],
        values[5],values[6],values[7],values[8],values[9],values[10],values[11],
        values[12],values[13],values[14],values[15],values[16],values[17],values[18],
        values[19],values[20],values[21],values[22],values[23],values[24],values[25],
        values[26],values[27],values[28],values[29],values[30],values[31]], dtype=np.int64)

        test_np_input = test_np_input.reshape(1, -1)
    
        preds = model.predict(test_np_input)
        
        rating = "E"
        if np.array_equiv(preds, np.array([[1,0,0,0]], dtype=np.int64)):
            rating = "E"
        if np.array_equiv(preds, np.array([[0,1,0,0]], dtype=np.int64)):
            rating = "ET"
        if np.array_equiv(preds, np.array([[0,0,1,0]], dtype=np.int64)):
            rating = "M"
        if np.array_equiv(preds, np.array([[0,0,0,1]], dtype=np.int64)):
            rating = "T"


        #[1,0,0,0] = E
        #[0,1,0,0] = ET
        #[0,0,1,0] = M
        #[0,0,0,1] = T
        session['Rating'] = rating
        #return "The rating for this game is: " + rating + " " + str(preds)
        return redirect(url_for('rating'))
    
@app.route('/rating/')
def rating():
    value = session.get('Rating', None)
    return render_template('rating.html', data=value)

if __name__ == '__main__':
    app.run()
    
