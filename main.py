from flask import Flask,render_template,request,redirect
import searchbykey,io,base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
matplotlib.use('Agg')

server = Flask(__name__)

#main page
@server.route("/") 
def firstpage():
    return render_template('index.html')

#page for showing the result of query seach.
@server.route("/showlistpage",methods=['POST']) 
def showlistpage():
    if request.method=="POST":
        query=request.form['keyword']
        query_results=searchbykey.show_list(query)
        num=len(query_results['video_title'])
        return render_template('showlistpage.html',datas=query_results,len=num,keyword=query)

#About
@server.route("/about")
def output_test():
    return render_template('contact.html')   

#page for show plot from output sentiment analysis
@server.route("/choosevideo",methods=['POST'])
def choosevideo():
    if request.method=="POST":
        keyword=request.form['keyword']
        row=int(request.form['row'])
        video=searchbykey.choosevideo(keyword,row)
        data=searchbykey.sentiment(video)
    #get data in form of dataframe
        count_class=data['class'].value_counts().to_frame()
    
    #generate plot
        pngImage=count_class.plot.pie(y='class',autopct="%.1f%%",colors=['darkslategray','darkturquoise'],shadow=True,figsize=(10,10),textprops={'fontsize': 14}).get_figure()
    #save plot in base64 for bringing the plot to html file without saving in png
        buf = io.BytesIO()
        pngImage.savefig(buf,format='png',transparent=True)
        buf.seek(0)
        buffer=b''.join(buf)
        pngImageB64String=base64.b64encode(buffer).decode('utf8') 


        plt.clf()
        fig=searchbykey.wordcloud(data)
        buf2 = io.BytesIO()

        fig.savefig(buf2,format='png',transparent=True)
        buf2.seek(0)
        buffer2=b''.join(buf2)
        pngImageB64String_2=base64.b64encode(buffer2).decode('utf8') 

        num=len(data)
    return render_template("showlistpage.html",image=pngImageB64String,image2=pngImageB64String_2,datas=data,len=num)

if __name__ == "__main__":
    server.run(debug=True)