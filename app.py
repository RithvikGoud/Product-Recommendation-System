from flask import Flask,render_template,request
import pickle
import numpy as np

top_discount_df=pickle.load(open(r"C:\Users\ganesh\Desktop\Product_Recommendation_System\Top_discount.pkl",'rb'))
df=pickle.load(open(r"C:\Users\ganesh\Desktop\Product_Recommendation_System\df.pkl",'rb'))
similarity=pickle.load(open(r"C:\Users\ganesh\Desktop\Product_Recommendation_System\similarity.pkl",'rb'))

app=Flask(__name__,static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html',
                           Category=list(top_discount_df['Product Category'].values),
                           Sub_Category=list(top_discount_df['Product_Sub_Category'].values),
                           Product_Name=list(top_discount_df['Product_Name'].values),
                           Product_Discount=list(top_discount_df['Discount'].values),
                           link=list(top_discount_df['Img_Link'].values),)


@app.route('/recommend_products',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    product_index = df[df["Product_Name"] == user_input].index[0]
    distances = similarity[product_index]
    product_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:300]
    
    printed_products = set()
    printed_count = 0 
    
    product_data=[]
    for i in product_list:
        product_name = df.iloc[i[0]].Product_Name
        img_Link = df.iloc[i[0]].Img_Link
        Product_Sub_Category = df.iloc[i[0]].Product_Sub_Category
        discount = "{:.0f}%".format(df.iloc[i[0]].Discount)
        
        if product_name not in printed_products:
            product_lists=[product_name,img_Link,Product_Sub_Category, discount]
            product_data.append(product_lists)
            printed_products.add(product_name)
            printed_count += 1
            if printed_count >= 5:
                break
    print(product_data)

    return render_template('index.html',data=product_data)

    

if __name__=='__main__':
    app.run(debug=True)