from flask import Flask,redirect,request,render_template,jsonify
import pandas as pd
import os
app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['MAX_CONTENT_LENGTH']=16*1024*1024

# command for profile page
@app.route("/profiles",methods=["GET","POST"])
def profile():
    df=pd.read_csv("up.csv")
    books_info=[]
    for i in range(len(df)):
        html=f"""
        <div style='display:flex; flex-direction:column; margin:0px;'>
            <Label style='font-size:35px; margin:2px;'>{df['title'][i]}</Label>
            <Label style='font-size:20px; margin:2px; color:grey; word-wrap:break-word; white-space:normal;'>{df['description'][i]}</Label>
            <section style='display:flex;'>
                <form action='/showfile' style='margin:10px;' method='post'>
                    <button style='color:white; background-color:rgb(139, 96, 225); border-radius:5px; font-size: 22.5px;' method='get' name='read_file' value="{i}">read {df['title'][i]}</button>
                </form>
                <form action='/update' style='margin:10px;' method='post'>
                    <button style='color:white; background-color: blue; font-size:22.5px; border-radius:5px;' method='get' name='upd_file' value="{i}">Update {df['title'][i]}</button>
                </form>
                <form action='/delete' style='margin:10px;' method='post'>
                    <button style='color:white; background-color: red; font-size:22.5px; border-radius:5px;' method='get' name='del_file' value="{i}">Delete {df['title'][i]}</button>
                </form>
            </section>
        </div>
        <hr style='height:2px; background-color:grey; margin:0px;'>
        """
        books_info.append(html)
    total_html="<br>".join(books_info)
    return render_template("profile.html",output=total_html)

#program for Home page
@app.route("/",methods=["GET","POST"])
def home():
    df=pd.read_csv("database/all.csv")
    books_info=[]
    for i in range(len(df)):
        print(df["title"][i])
        html=f"""

            <div class="content" style='display:flex; flex-direction:column; margin-left:5px; width:100%;'>
                <label style='font-size:40px; margin:2px;'>{df['title'][i]}</label>
                <label style='font-size:20px; margin:2px; word-wrap:break-word; white-space:normal;'>{df['description'][i]}</label>
                <form action='/showfile' style='margin:10px;' method='post' >
                    <button style='color:white; background-color: rgb(139, 96, 225); font-size:25px; border-radius:5px;' method='get' name='read_file' value="{i}">read {df['title'][i]}</button>
                </form> 
            </div>
        
        <hr style='height:2px; background-color:grey; margin:0px; width:100%;'>
        """
        books_info.append(html)
    total_html="<br>".join(books_info)
    return render_template("index.html",output=total_html)

#program for upload page
@app.route("/upload",methods=["GET","POST"])
def upload():
    return render_template("upload.html")
#program for uploading books/files 
@app.route("/files",methods=["GET","POST"])
def file():
    df=pd.read_csv("database/all.csv")
    title=request.form.get("title")
    description=request.form.get("summary")
    print(description)
    print(title)
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}),400
    file=request.files["file"]
    if file.filename == '':
        return jsonify({"error":"No selected file"}),400
    if file:
        filepath=f"bookfiles/{file.filename}"
        file.save(filepath)
        print(filepath)
        index=len(df)+1
        df.loc[index,"title"]=title
        df.loc[index,"description"]=description
        df.loc[index,"path"]=filepath
        df.to_csv("up.csv",index=False)
        df.to_csv("database/all.csv",index=False)
        print(df)
        return "file uploaded"
    
#program for reading files
@app.route("/showfile",methods=["GET","POST"])
def show():
    df=pd.read_csv("up.csv")
    text=request.form["read_file"]
    text=int(text)
    path=df['path'][text]
    path=os.path.abspath(path)
    os.startfile(path)
    return """<section style=' display:flex; flex-direction:column; justify-content:center; align-content:center; justify-items:center; align-items:center;'><Label style='font-size:25px'>Help us with your review</Label><input style='border-radius:5px; padding:10px; margin:10px; width:50%;' type='text'></section>"""

#program for deleting books/files
@app.route("/delete",methods=["GET","POST"])
def deletebook():
    df=pd.read_csv("up.csv")

    textdel=request.form["del_file"]
    df.drop(int(textdel),inplace=True)
    df.to_csv("up.csv",index=False)
    df.to_csv("database/all.csv")
    return "Book deleted successfully"

#program for update page of the book details
@app.route("/update",methods=["GET","POST"])
def updatebook():
    update_form="""
    <form action='/updates' method="post">
        <Label>Enter the book name you want to update :</Label>
        <input type="text" name="bookname" id="bookname">
        <Label>Update Book name :</Label>
        <input type="text" name="updname" id="updname">
        <Label>Update Book description :</Label>
        <input type="text" name="upddis" id="upddis">
        <input type="submit">
    </form>
    """
    global index
    index=request.form["upd_file"]
    return update_form

#program to update the book details
@app.route("/updates",methods=["GET","POST"])
def upd():
    updname=request.form.get("updname")
    upddis=request.form.get("upddis")
    bookname=request.form.get("bookname")
    df=pd.read_csv("up.csv")
    print(df["title"])
    for i in range(len(df)):
        if df.iloc[i]["title"]==bookname:
            index=i
            print("index is",i)
    if len(updname)!=0:
        df["title"][index]=updname
    if len(upddis)!=0:
        df["description"][index]=upddis
    df.to_csv("up.csv",index=False)
    df.to_csv("database/all.csv",index=False)
    return """<body><section style='background-color: rgb(176, 221, 176); height:50vh; display:flex; justify-items:center; align-content:center; align-items:center; justify-content:center;'> <Label style='color:white; font-size:25px;'> Changes have been saved </Label> </section></body>"""

#program for searching books
@app.route("/Searchquery",methods=["GET","POST"])
def Search():
    df=pd.read_csv("database/all.csv")
    search=request.form.get("Search")
    print(search)
    from rapidfuzz import process
    match=process.extractOne(search,list(df["title"]))
    print(match)
    for i in range(len(df)):
        if df["title"][i]==match[0]:
            index=i
            print("index",index)
    match=match[0]
    html=f"""
        <div class="content" style='display:flex; flex-direction:column; margin-left:5px; width:100%;'>
            <label style='font-size:40px; margin:2px;'>{df['title'][index]}</label>
            <label style='font-size:20px; margin:2px; word-wrap:break-word; white-space:normal;'>{df['description'][index]}</label>
            <form action='/showfile' style='margin:10px;' method='post' >
                <button style='color:white; background-color: rgb(139, 96, 225); font-size:25px; border-radius:5px;' method='get' name='read_file' value="{index}">read {df['title'][index]}</button>
            </form> 
        </div>
        
        <hr style='height:2px; background-color:grey; margin:0px; width:100%;'>
    """
    for i in os.listdir("/bookfiles"):
        print(i)
    return html


if __name__=="__main__":
    app.run(debug=True)