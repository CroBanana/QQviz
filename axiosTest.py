from flask import Flask,Response,jsonify,request,flash,render_template,current_app,redirect

app=Flask(__name__)
app.secret_key = "UGABUGASTIKVALABLJAT"

@app.route('/axios', methods=['POST','get'])
def test():
    
    return render_template("axiosTest.html")
    
if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)